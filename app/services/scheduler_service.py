"""Scheduler service for managing jobs and executions"""
from models.job import Job, JobExecution
from services.jobs import get_job_class, get_available_jobs
from typing import List, Dict, Optional
from datetime import datetime
from bson import ObjectId
import traceback
import asyncio
from threading import Thread


class SchedulerService:
    """Service for managing scheduled jobs"""
    
    # In-memory scheduler for background execution
    _scheduler = None
    _executor_thread = None
    
    @staticmethod
    def initialize_scheduler():
        """Initialize the scheduler"""
        try:
            Job.create_indexes()
            JobExecution.create_indexes()
            return True
        except Exception as e:
            print(f"Error initializing scheduler: {e}")
            return False
    
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
            
            job_id = Job.insert_job(job_data)
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
            
            Job.update_job(job_id, job_data)
            
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
            
            Job.delete_job(job_id)
            
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
        """Execute a job immediately"""
        try:
            job = Job.find_job_by_id(job_id)
            if not job:
                return {
                    "success": False,
                    "message": "Job not found",
                    "execution_id": None
                }
            
            # Create execution record
            execution_data = {
                "job_id": job_id,
                "user_id": str(job["user_id"]),
                "job_name": job["name"],
                "job_class_string": job["job_class_string"],
                "status": "running",
                "output": "",
                "error": "",
                "started_at": datetime.utcnow()
            }
            
            execution_id = JobExecution.insert_execution(execution_data)
            
            # Execute the job in background
            def execute_job_background():
                try:
                    job_class = get_job_class(job["job_class_string"])
                    if job_class:
                        job_instance = job_class(
                            pub_args=job.get("pub_args", []),
                            pub_kwargs=job.get("pub_kwargs", {})
                        )
                        output = job_instance.run()
                        
                        # Update execution with success
                        JobExecution.update_execution(str(execution_id), {
                            "status": "completed",
                            "output": output,
                            "completed_at": datetime.utcnow()
                        })
                        
                        # Update job stats
                        Job.update_job(job_id, {
                            "last_run_time": datetime.utcnow(),
                            "total_executions": job.get("total_executions", 0) + 1
                        })
                    else:
                        JobExecution.update_execution(str(execution_id), {
                            "status": "failed",
                            "error": "Job class not found",
                            "completed_at": datetime.utcnow()
                        })
                except Exception as e:
                    JobExecution.update_execution(str(execution_id), {
                        "status": "failed",
                        "error": str(e) + "\n" + traceback.format_exc(),
                        "completed_at": datetime.utcnow()
                    })
            
            # Start job in background thread
            thread = Thread(target=execute_job_background, daemon=True)
            thread.start()
            
            return {
                "success": True,
                "message": "Job execution started",
                "execution_id": str(execution_id)
            }
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
