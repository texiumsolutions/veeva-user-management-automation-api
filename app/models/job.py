"""Job model for MongoDB - Scheduler jobs"""
from pymongo import ASCENDING
from core.database import get_db
from datetime import datetime
from bson import ObjectId
from typing import Optional, List, Dict


class Job:
    """Job model for MongoDB storage - represents scheduled jobs"""
    
    def __init__(self, 
                 user_id: str,
                 job_class_string: str,
                 name: str,
                 description: Optional[str] = None,
                 pub_args: Optional[List] = None,
                 pub_kwargs: Optional[Dict] = None,
                 minute: str = "*",
                 hour: str = "*",
                 day_of_month: str = "*",
                 month: str = "*",
                 day_of_week: str = "*",
                 week: str = "*",
                 is_enabled: bool = True,
                 is_paused: bool = False):
        self.user_id = user_id
        self.job_class_string = job_class_string
        self.name = name
        self.description = description or ""
        self.pub_args = pub_args or []
        self.pub_kwargs = pub_kwargs or {}
        self.minute = minute
        self.hour = hour
        self.day_of_month = day_of_month
        self.month = month
        self.day_of_week = day_of_week
        self.week = week
        self.is_enabled = is_enabled
        self.is_paused = is_paused
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    @staticmethod
    def create_indexes():
        """Create indexes on jobs collection"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        jobs_collection.create_index([("user_id", ASCENDING)])
        jobs_collection.create_index([("name", ASCENDING)])
        jobs_collection.create_index([("is_enabled", ASCENDING)])
    
    @staticmethod
    def insert_job(job_data: dict):
        """Insert a new job into MongoDB"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        
        job_doc = {
            "user_id": ObjectId(job_data.get("user_id")) if isinstance(job_data.get("user_id"), str) else job_data.get("user_id"),
            "job_class_string": job_data.get("job_class_string"),
            "name": job_data.get("name"),
            "description": job_data.get("description", ""),
            "pub_args": job_data.get("pub_args", []),
            "pub_kwargs": job_data.get("pub_kwargs", {}),
            "minute": job_data.get("minute", "*"),
            "hour": job_data.get("hour", "*"),
            "day_of_month": job_data.get("day_of_month", "*"),
            "month": job_data.get("month", "*"),
            "day_of_week": job_data.get("day_of_week", "*"),
            "week": job_data.get("week", "*"),
            "is_enabled": job_data.get("is_enabled", True),
            "is_paused": job_data.get("is_paused", False),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "last_run_time": None,
            "next_run_time": None,
            "total_executions": 0
        }
        result = jobs_collection.insert_one(job_doc)
        return result.inserted_id
    
    @staticmethod
    def find_job_by_id(job_id: str):
        """Find a job by ID"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        try:
            return jobs_collection.find_one({"_id": ObjectId(job_id)})
        except:
            return None
    
    @staticmethod
    def find_all_jobs():
        """Find all jobs"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        return list(jobs_collection.find())
    
    @staticmethod
    def find_jobs_by_user(user_id: str):
        """Find all jobs for a specific user"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        try:
            user_obj_id = ObjectId(user_id) if isinstance(user_id, str) else user_id
            return list(jobs_collection.find({"user_id": user_obj_id}))
        except:
            return []
    
    @staticmethod
    def update_job(job_id: str, job_data: dict):
        """Update a job"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        
        update_data = {k: v for k, v in job_data.items() if k not in ["user_id", "_id", "created_at"]}
        update_data["updated_at"] = datetime.utcnow()
        
        try:
            result = jobs_collection.update_one({"_id": ObjectId(job_id)}, {"$set": update_data})
            return result.modified_count > 0
        except:
            return False
    
    @staticmethod
    def delete_job(job_id: str):
        """Delete a job"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        try:
            result = jobs_collection.delete_one({"_id": ObjectId(job_id)})
            return result.deleted_count > 0
        except:
            return False
    
    @staticmethod
    def pause_job(job_id: str):
        """Pause a job"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        try:
            result = jobs_collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": {"is_paused": True, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False
    
    @staticmethod
    def resume_job(job_id: str):
        """Resume a paused job"""
        db = get_db()
        jobs_collection = db['scheduler_jobs']
        try:
            result = jobs_collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": {"is_paused": False, "updated_at": datetime.utcnow()}}
            )
            return result.modified_count > 0
        except:
            return False


class JobExecution:
    """JobExecution model - represents a single job execution"""
    
    def __init__(self, 
                 job_id: str,
                 user_id: str,
                 job_name: str,
                 job_class_string: str,
                 status: str = "pending",
                 output: str = "",
                 error: str = ""):
        self.job_id = job_id
        self.user_id = user_id
        self.job_name = job_name
        self.job_class_string = job_class_string
        self.status = status  # pending, running, completed, failed
        self.output = output
        self.error = error
        self.started_at = None
        self.completed_at = None
        self.created_at = datetime.utcnow()
    
    @staticmethod
    def create_indexes():
        """Create indexes on executions collection"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        executions_collection.create_index([("user_id", ASCENDING)])
        executions_collection.create_index([("job_id", ASCENDING)])
        executions_collection.create_index([("created_at", ASCENDING)])
        executions_collection.create_index([("status", ASCENDING)])
    
    @staticmethod
    def insert_execution(execution_data: dict):
        """Insert a new execution record"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        
        execution_doc = {
            "job_id": ObjectId(execution_data.get("job_id")) if isinstance(execution_data.get("job_id"), str) else execution_data.get("job_id"),
            "user_id": ObjectId(execution_data.get("user_id")) if isinstance(execution_data.get("user_id"), str) else execution_data.get("user_id"),
            "job_name": execution_data.get("job_name"),
            "job_class_string": execution_data.get("job_class_string"),
            "status": execution_data.get("status", "pending"),
            "output": execution_data.get("output", ""),
            "error": execution_data.get("error", ""),
            "started_at": execution_data.get("started_at"),
            "completed_at": execution_data.get("completed_at"),
            "created_at": datetime.utcnow()
        }
        result = executions_collection.insert_one(execution_doc)
        return result.inserted_id
    
    @staticmethod
    def find_execution_by_id(execution_id: str):
        """Find an execution by ID"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        try:
            return executions_collection.find_one({"_id": ObjectId(execution_id)})
        except:
            return None
    
    @staticmethod
    def find_executions_by_job(job_id: str, limit: int = 50):
        """Find all executions for a job"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        try:
            job_obj_id = ObjectId(job_id) if isinstance(job_id, str) else job_id
            return list(executions_collection.find({"job_id": job_obj_id}).sort("created_at", -1).limit(limit))
        except:
            return []
    
    @staticmethod
    def find_executions_by_status(status: str, limit: int = 50):
        """Find all executions by status"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        return list(executions_collection.find({"status": status}).sort("created_at", -1).limit(limit))
    
    @staticmethod
    def update_execution(execution_id: str, execution_data: dict):
        """Update an execution record"""
        db = get_db()
        executions_collection = db['scheduler_executions']
        
        update_data = {k: v for k, v in execution_data.items() if k not in ["_id", "created_at"]}
        
        try:
            result = executions_collection.update_one({"_id": ObjectId(execution_id)}, {"$set": update_data})
            return result.modified_count > 0
        except:
            return False
