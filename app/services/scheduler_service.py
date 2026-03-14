"""Scheduler service for managing jobs and executions."""
from datetime import datetime
from threading import Lock, Thread
from typing import Dict, Optional
import traceback

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from bson import ObjectId

from models.job import Job, JobAuditLog, JobExecution
from services.jobs import get_available_jobs, get_job_class


class SchedulerService:
    """Service for managing scheduled jobs."""

    _scheduler = None
    _scheduler_lock = Lock()

    @staticmethod
    def initialize_scheduler():
        """Initialize indexes and start the in-process scheduler."""
        try:
            Job.create_indexes()
            JobExecution.create_indexes()
            JobAuditLog.create_indexes()

            with SchedulerService._scheduler_lock:
                if SchedulerService._scheduler is None:
                    SchedulerService._scheduler = BackgroundScheduler(timezone="UTC")
                    SchedulerService._scheduler.start()

            SchedulerService.sync_all_jobs()
            return True
        except Exception as e:
            print(f"Error initializing scheduler: {e}")
            return False

    @staticmethod
    def shutdown_scheduler():
        """Stop the in-process scheduler cleanly."""
        with SchedulerService._scheduler_lock:
            if SchedulerService._scheduler is not None:
                SchedulerService._scheduler.shutdown(wait=False)
                SchedulerService._scheduler = None

    @staticmethod
    def _build_trigger(job_data: dict) -> CronTrigger:
        """Build a cron trigger from persisted job fields."""
        return CronTrigger(
            minute=job_data.get("minute", "*"),
            hour=job_data.get("hour", "*"),
            day=job_data.get("day_of_month", "*"),
            month=job_data.get("month", "*"),
            day_of_week=job_data.get("day_of_week", "*"),
            week=job_data.get("week", "*"),
            timezone="UTC",
        )

    @staticmethod
    def _remove_scheduled_job(job_id: str):
        """Remove a scheduled APScheduler job if it exists."""
        if SchedulerService._scheduler is None:
            return

        existing_job = SchedulerService._scheduler.get_job(job_id)
        if existing_job:
            SchedulerService._scheduler.remove_job(job_id)

    @staticmethod
    def _sync_job_to_scheduler(job_data: dict):
        """Create, update, or remove the APScheduler job for a stored job."""
        if SchedulerService._scheduler is None:
            return

        job_id = str(job_data["_id"])
        should_schedule = job_data.get("is_enabled", True) and not job_data.get("is_paused", False)

        if not should_schedule:
            SchedulerService._remove_scheduled_job(job_id)
            Job.update_job(job_id, {"next_run_time": None})
            return

        trigger = SchedulerService._build_trigger(job_data)
        scheduled_job = SchedulerService._scheduler.add_job(
            SchedulerService._run_job_from_scheduler,
            trigger=trigger,
            args=[job_id],
            id=job_id,
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=60,
        )
        Job.update_job(job_id, {"next_run_time": scheduled_job.next_run_time})

    @staticmethod
    def sync_all_jobs():
        """Restore all persisted jobs into APScheduler."""
        jobs = Job.find_all_jobs()
        for job in jobs:
            SchedulerService._sync_job_to_scheduler(job)

    @staticmethod
    def _run_job_from_scheduler(job_id: str):
        """Entry point used by APScheduler."""
        SchedulerService._execute_job(job_id, trigger_type="scheduled")

    @staticmethod
    def _serialize_audit_log(log: dict) -> Dict:
        """Convert an audit log document into an API-friendly dict."""
        return {
            "_id": str(log["_id"]),
            "job_id": str(log["job_id"]) if log.get("job_id") else None,
            "user_id": str(log["user_id"]) if log.get("user_id") else None,
            "job_name": log.get("job_name"),
            "job_class_string": log.get("job_class_string"),
            "event_type": log.get("event_type"),
            "trigger_type": log.get("trigger_type"),
            "status": log.get("status"),
            "message": log.get("message", ""),
            "details": log.get("details", {}),
            "execution_id": str(log["execution_id"]) if log.get("execution_id") else None,
            "created_at": log.get("created_at"),
        }

    @staticmethod
    def _create_audit_log(
        job: dict,
        event_type: str,
        message: str,
        status: str = "info",
        trigger_type: Optional[str] = None,
        details: Optional[Dict] = None,
        execution_id: Optional[str] = None,
    ):
        """Persist a scheduler audit event."""
        JobAuditLog.insert_log({
            "job_id": str(job["_id"]) if job.get("_id") else None,
            "user_id": str(job["user_id"]) if job.get("user_id") else None,
            "job_name": job.get("name"),
            "job_class_string": job.get("job_class_string"),
            "event_type": event_type,
            "trigger_type": trigger_type,
            "status": status,
            "message": message,
            "details": details or {},
            "execution_id": execution_id,
        })

    @staticmethod
    def _execute_job(job_id: str, trigger_type: str = "manual") -> Dict:
        """Create an execution record and run the job in a background thread."""
        job = Job.find_job_by_id(job_id)
        if not job:
            return {
                "success": False,
                "message": "Job not found",
                "execution_id": None,
            }

        execution_data = {
            "job_id": job_id,
            "user_id": str(job["user_id"]),
            "job_name": job["name"],
            "job_class_string": job["job_class_string"],
            "status": "running",
            "output": "",
            "error": "",
            "started_at": datetime.utcnow(),
        }
        execution_id = JobExecution.insert_execution(execution_data)
        SchedulerService._create_audit_log(
            job,
            event_type="job_triggered",
            message=f"Job '{job['name']}' triggered via {trigger_type} run",
            trigger_type=trigger_type,
            status="info",
            execution_id=str(execution_id),
            details={
                "pub_args": job.get("pub_args", []),
                "pub_kwargs": job.get("pub_kwargs", {}),
            },
        )

        def execute_job_background():
            try:
                job_class = get_job_class(job["job_class_string"])
                if not job_class:
                    raise ValueError(f"Job class '{job['job_class_string']}' not found")

                job_instance = job_class(
                    pub_args=job.get("pub_args", []),
                    pub_kwargs=job.get("pub_kwargs", {}),
                )
                output = job_instance.run()
                completed_at = datetime.utcnow()

                JobExecution.update_execution(str(execution_id), {
                    "status": "completed",
                    "output": output,
                    "completed_at": completed_at,
                })

                latest_job = Job.find_job_by_id(job_id) or job
                next_run_time = None
                if SchedulerService._scheduler is not None:
                    scheduled_job = SchedulerService._scheduler.get_job(job_id)
                    if scheduled_job:
                        next_run_time = scheduled_job.next_run_time

                Job.update_job(job_id, {
                    "last_run_time": completed_at,
                    "next_run_time": next_run_time,
                    "total_executions": latest_job.get("total_executions", 0) + 1,
                })
                SchedulerService._create_audit_log(
                    job,
                    event_type="job_completed",
                    message=f"Job '{job['name']}' completed successfully",
                    trigger_type=trigger_type,
                    status="success",
                    execution_id=str(execution_id),
                    details={
                        "completed_at": completed_at.isoformat(),
                        "next_run_time": next_run_time.isoformat() if next_run_time else None,
                    },
                )
            except Exception as e:
                JobExecution.update_execution(str(execution_id), {
                    "status": "failed",
                    "error": str(e) + "\n" + traceback.format_exc(),
                    "completed_at": datetime.utcnow(),
                })

                next_run_time = None
                if SchedulerService._scheduler is not None:
                    scheduled_job = SchedulerService._scheduler.get_job(job_id)
                    if scheduled_job:
                        next_run_time = scheduled_job.next_run_time

                Job.update_job(job_id, {
                    "next_run_time": next_run_time,
                })
                SchedulerService._create_audit_log(
                    job,
                    event_type="job_failed",
                    message=f"Job '{job['name']}' failed during execution",
                    trigger_type=trigger_type,
                    status="failed",
                    execution_id=str(execution_id),
                    details={
                        "error": str(e),
                        "next_run_time": next_run_time.isoformat() if next_run_time else None,
                    },
                )

        thread = Thread(target=execute_job_background, daemon=True)
        thread.start()

        return {
            "success": True,
            "message": "Job execution started",
            "execution_id": str(execution_id),
        }
    
    @staticmethod
    def create_job(job_data: dict) -> Dict:
        """
        Create a new scheduled job
        """
        try:
            # Validate required fields
            required_fields = ["user_id", "job_class_string", "name"]
            for field in required_fields:
                if not job_data.get(field):
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}",
                        "job_id": None
                    }
            
            # Validate job class exists
            job_class = get_job_class(job_data.get("job_class_string"))
            if not job_class:
                return {
                    "success": False,
                    "message": f"Job class '{job_data.get('job_class_string')}' not found",
                    "job_id": None
                }
            
            SchedulerService._build_trigger(job_data)

            job_id = Job.insert_job(job_data)
            created_job = Job.find_job_by_id(str(job_id))
            if created_job:
                SchedulerService._sync_job_to_scheduler(created_job)
                SchedulerService._create_audit_log(
                    created_job,
                    event_type="job_created",
                    message=f"Job '{created_job['name']}' created",
                    status="success",
                    details={
                        "schedule": {
                            "minute": created_job.get("minute", "*"),
                            "hour": created_job.get("hour", "*"),
                            "day_of_month": created_job.get("day_of_month", "*"),
                            "month": created_job.get("month", "*"),
                            "day_of_week": created_job.get("day_of_week", "*"),
                            "week": created_job.get("week", "*"),
                        },
                    },
                )
            return {
                "success": True,
                "message": f"Job '{job_data.get('name')}' created successfully",
                "job_id": str(job_id)
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "job_id": None
            }
    
    @staticmethod
    def get_job(job_id: str) -> Dict:
        """Get a job by ID"""
        try:
            job = Job.find_job_by_id(job_id)
            if not job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "data": None
                }
            
            # Convert ObjectId to string
            job_data = {
                "_id": str(job["_id"]),
                "user_id": str(job["user_id"]),
                "job_class_string": job["job_class_string"],
                "name": job["name"],
                "description": job.get("description", ""),
                "pub_args": job.get("pub_args", []),
                "pub_kwargs": job.get("pub_kwargs", {}),
                "minute": job.get("minute", "*"),
                "hour": job.get("hour", "*"),
                "day_of_month": job.get("day_of_month", "*"),
                "month": job.get("month", "*"),
                "day_of_week": job.get("day_of_week", "*"),
                "week": job.get("week", "*"),
                "is_enabled": job.get("is_enabled", True),
                "is_paused": job.get("is_paused", False),
                "created_at": job.get("created_at"),
                "updated_at": job.get("updated_at"),
                "last_run_time": job.get("last_run_time"),
                "next_run_time": job.get("next_run_time"),
                "total_executions": job.get("total_executions", 0)
            }
            
            return {
                "success": True,
                "message": "Job retrieved successfully",
                "data": job_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def get_all_jobs() -> Dict:
        """Get all jobs"""
        try:
            jobs = Job.find_all_jobs()
            
            jobs_data = []
            for job in jobs:
                job_data = {
                    "_id": str(job["_id"]),
                    "user_id": str(job["user_id"]),
                    "job_class_string": job["job_class_string"],
                    "name": job["name"],
                    "description": job.get("description", ""),
                    "pub_args": job.get("pub_args", []),
                    "pub_kwargs": job.get("pub_kwargs", {}),
                    "minute": job.get("minute", "*"),
                    "hour": job.get("hour", "*"),
                    "day_of_month": job.get("day_of_month", "*"),
                    "month": job.get("month", "*"),
                    "day_of_week": job.get("day_of_week", "*"),
                    "week": job.get("week", "*"),
                    "is_enabled": job.get("is_enabled", True),
                    "is_paused": job.get("is_paused", False),
                    "created_at": job.get("created_at"),
                    "updated_at": job.get("updated_at"),
                    "last_run_time": job.get("last_run_time"),
                    "next_run_time": job.get("next_run_time"),
                    "total_executions": job.get("total_executions", 0)
                }
                jobs_data.append(job_data)
            
            return {
                "success": True,
                "message": "Jobs retrieved successfully",
                "total": len(jobs_data),
                "data": jobs_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": []
            }
    
    @staticmethod
    def get_jobs_by_user(user_id: str) -> Dict:
        """Get all jobs for a specific user"""
        try:
            jobs = Job.find_jobs_by_user(user_id)
            
            jobs_data = []
            for job in jobs:
                job_data = {
                    "_id": str(job["_id"]),
                    "user_id": str(job["user_id"]),
                    "job_class_string": job["job_class_string"],
                    "name": job["name"],
                    "description": job.get("description", ""),
                    "pub_args": job.get("pub_args", []),
                    "pub_kwargs": job.get("pub_kwargs", {}),
                    "minute": job.get("minute", "*"),
                    "hour": job.get("hour", "*"),
                    "day_of_month": job.get("day_of_month", "*"),
                    "month": job.get("month", "*"),
                    "day_of_week": job.get("day_of_week", "*"),
                    "week": job.get("week", "*"),
                    "is_enabled": job.get("is_enabled", True),
                    "is_paused": job.get("is_paused", False),
                    "created_at": job.get("created_at"),
                    "updated_at": job.get("updated_at"),
                    "last_run_time": job.get("last_run_time"),
                    "next_run_time": job.get("next_run_time"),
                    "total_executions": job.get("total_executions", 0)
                }
                jobs_data.append(job_data)
            
            return {
                "success": True,
                "message": "Jobs retrieved successfully",
                "total": len(jobs_data),
                "data": jobs_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": []
            }
    
    @staticmethod
    def update_job(job_id: str, job_data: dict) -> Dict:
        """Update a job"""
        try:
            existing_job = Job.find_job_by_id(job_id)
            if not existing_job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "job_id": None
                }
            
            # If job_class_string is being updated, validate it
            if "job_class_string" in job_data:
                job_class = get_job_class(job_data["job_class_string"])
                if not job_class:
                    return {
                        "success": False,
                        "message": f"Job class '{job_data['job_class_string']}' not found",
                        "job_id": None
                    }
            
            merged_job = {**existing_job, **job_data}
            SchedulerService._build_trigger(merged_job)

            Job.update_job(job_id, job_data)
            refreshed_job = Job.find_job_by_id(job_id)
            if refreshed_job:
                SchedulerService._sync_job_to_scheduler(refreshed_job)
                SchedulerService._create_audit_log(
                    refreshed_job,
                    event_type="job_modified",
                    message=f"Job '{refreshed_job['name']}' updated",
                    status="success",
                    details={
                        "updated_fields": job_data,
                    },
                )
            
            return {
                "success": True,
                "message": "Job updated successfully",
                "job_id": job_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "job_id": None
            }
    
    @staticmethod
    def delete_job(job_id: str) -> Dict:
        """Delete a job"""
        try:
            existing_job = Job.find_job_by_id(job_id)
            if not existing_job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "job_id": None
                }
            
            SchedulerService._remove_scheduled_job(job_id)
            Job.delete_job(job_id)
            SchedulerService._create_audit_log(
                existing_job,
                event_type="job_deleted",
                message=f"Job '{existing_job['name']}' deleted",
                status="success",
            )
            
            return {
                "success": True,
                "message": "Job deleted successfully",
                "job_id": job_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "job_id": None
            }
    
    @staticmethod
    def pause_job(job_id: str) -> Dict:
        """Pause a job"""
        try:
            existing_job = Job.find_job_by_id(job_id)
            if not existing_job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "job_id": None
                }
            
            Job.pause_job(job_id)
            paused_job = Job.find_job_by_id(job_id)
            if paused_job:
                SchedulerService._sync_job_to_scheduler(paused_job)
                SchedulerService._create_audit_log(
                    paused_job,
                    event_type="job_paused",
                    message=f"Job '{paused_job['name']}' paused",
                    status="success",
                )
            
            return {
                "success": True,
                "message": "Job paused successfully",
                "job_id": job_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "job_id": None
            }
    
    @staticmethod
    def resume_job(job_id: str) -> Dict:
        """Resume a paused job"""
        try:
            existing_job = Job.find_job_by_id(job_id)
            if not existing_job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "job_id": None
                }
            
            Job.resume_job(job_id)
            resumed_job = Job.find_job_by_id(job_id)
            if resumed_job:
                SchedulerService._sync_job_to_scheduler(resumed_job)
                SchedulerService._create_audit_log(
                    resumed_job,
                    event_type="job_resumed",
                    message=f"Job '{resumed_job['name']}' resumed",
                    status="success",
                    details={
                        "next_run_time": resumed_job.get("next_run_time").isoformat() if resumed_job.get("next_run_time") else None,
                    },
                )
            
            return {
                "success": True,
                "message": "Job resumed successfully",
                "job_id": job_id
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "job_id": None
            }
    
    @staticmethod
    def run_job_now(job_id: str) -> Dict:
        """Execute a job immediately."""
        try:
            return SchedulerService._execute_job(job_id, trigger_type="manual")
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "execution_id": None
            }
    
    @staticmethod
    def get_executions(job_id: Optional[str] = None, limit: int = 50) -> Dict:
        """Get executions"""
        try:
            if job_id:
                executions = JobExecution.find_executions_by_job(job_id, limit)
            else:
                from core.database import get_db
                db = get_db()
                executions_collection = db['scheduler_executions']
                executions = list(executions_collection.find().sort("created_at", -1).limit(limit))
            
            executions_data = []
            for execution in executions:
                execution_data = {
                    "_id": str(execution["_id"]),
                    "job_id": str(execution["job_id"]),
                    "user_id": str(execution["user_id"]),
                    "job_name": execution["job_name"],
                    "job_class_string": execution["job_class_string"],
                    "status": execution["status"],
                    "output": execution.get("output", ""),
                    "error": execution.get("error", ""),
                    "started_at": execution.get("started_at"),
                    "completed_at": execution.get("completed_at"),
                    "created_at": execution.get("created_at")
                }
                executions_data.append(execution_data)
            
            return {
                "success": True,
                "message": "Executions retrieved successfully",
                "total": len(executions_data),
                "data": executions_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": []
            }
    
    @staticmethod
    def get_execution(execution_id: str) -> Dict:
        """Get a specific execution"""
        try:
            execution = JobExecution.find_execution_by_id(execution_id)
            if not execution:
                return {
                    "success": False,
                    "message": "Execution not found",
                    "data": None
                }
            
            execution_data = {
                "_id": str(execution["_id"]),
                "job_id": str(execution["job_id"]),
                "user_id": str(execution["user_id"]),
                "job_name": execution["job_name"],
                "job_class_string": execution["job_class_string"],
                "status": execution["status"],
                "output": execution.get("output", ""),
                "error": execution.get("error", ""),
                "started_at": execution.get("started_at"),
                "completed_at": execution.get("completed_at"),
                "created_at": execution.get("created_at")
            }
            
            return {
                "success": True,
                "message": "Execution retrieved successfully",
                "data": execution_data
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": None
            }

    @staticmethod
    def get_audit_logs(job_id: Optional[str] = None, event_type: Optional[str] = None, limit: int = 100) -> Dict:
        """Get scheduler audit logs."""
        try:
            logs = JobAuditLog.find_logs(job_id=job_id, event_type=event_type, limit=limit)
            logs_data = [SchedulerService._serialize_audit_log(log) for log in logs]
            return {
                "success": True,
                "message": "Audit logs retrieved successfully",
                "total": len(logs_data),
                "data": logs_data,
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": [],
            }

    @staticmethod
    def get_audit_log(log_id: str) -> Dict:
        """Get a specific scheduler audit log."""
        try:
            log = JobAuditLog.find_log_by_id(log_id)
            if not log:
                return {
                    "success": False,
                    "message": "Audit log not found",
                    "data": None,
                }

            return {
                "success": True,
                "message": "Audit log retrieved successfully",
                "data": SchedulerService._serialize_audit_log(log),
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": None,
            }
    
    @staticmethod
    def get_available_jobs() -> Dict:
        """Get all available job classes"""
        try:
            jobs = get_available_jobs()
            
            jobs_list = []
            for class_string, job_info in jobs.items():
                jobs_list.append({
                    "class_string": class_string,
                    "name": job_info["name"],
                    "description": job_info["description"]
                })
            
            return {
                "success": True,
                "message": "Available jobs retrieved successfully",
                "total": len(jobs_list),
                "jobs": jobs_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "jobs": []
            }
    
    @staticmethod
    def get_scheduler_stats(user_id: Optional[str] = None) -> Dict:
        """Get scheduler statistics"""
        try:
            from core.database import get_db
            db = get_db()
            
            if user_id:
                user_obj_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
                total_jobs = db['scheduler_jobs'].count_documents({"user_id": user_obj_id})
                enabled_jobs = db['scheduler_jobs'].count_documents({"user_id": user_obj_id, "is_enabled": True})
                paused_jobs = db['scheduler_jobs'].count_documents({"user_id": user_obj_id, "is_paused": True})
                total_executions = db['scheduler_executions'].count_documents({"user_id": user_obj_id})
                completed_executions = db['scheduler_executions'].count_documents({"user_id": user_obj_id, "status": "completed"})
                failed_executions = db['scheduler_executions'].count_documents({"user_id": user_obj_id, "status": "failed"})
            else:
                total_jobs = db['scheduler_jobs'].count_documents({})
                enabled_jobs = db['scheduler_jobs'].count_documents({"is_enabled": True})
                paused_jobs = db['scheduler_jobs'].count_documents({"is_paused": True})
                total_executions = db['scheduler_executions'].count_documents({})
                completed_executions = db['scheduler_executions'].count_documents({"status": "completed"})
                failed_executions = db['scheduler_executions'].count_documents({"status": "failed"})
            
            return {
                "success": True,
                "message": "Stats retrieved successfully",
                "stats": {
                    "total_jobs": total_jobs,
                    "enabled_jobs": enabled_jobs,
                    "paused_jobs": paused_jobs,
                    "total_executions": total_executions,
                    "completed_executions": completed_executions,
                    "failed_executions": failed_executions,
                    "success_rate": (completed_executions / total_executions * 100) if total_executions > 0 else 0
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "stats": {}
            }
