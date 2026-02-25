"""Scheduler routes for API endpoints"""
from fastapi import APIRouter, HTTPException, Query
from schemas.job import (
    JobCreateRequest, JobUpdateRequest, JobListResponse,
    JobDetailResponse, ExecutionListResponse, ExecutionDetailResponse,
    JobActionResponse, ExecutionRunResponse, AvailableJobsResponse,
    JobStatsResponse
)
from services.scheduler_service import SchedulerService
from typing import Dict, Optional

# Initialize scheduler
SchedulerService.initialize_scheduler()

router = APIRouter(prefix="/api/scheduler", tags=["scheduler"])


# =================== Jobs Endpoints ===================

@router.post("/jobs", response_model=Dict)
async def create_job(job_data: JobCreateRequest):
    """
    Create a new scheduled job
    
    Required fields:
    - user_id: User ID who owns this job
    - job_class_string: Full path to job class (e.g., 'jobs.echo.EchoJob')
    - name: Job name
    
    Optional cron fields (default to "*"):
    - minute, hour, day_of_month, month, day_of_week, week
    - pub_args: List of positional arguments
    - pub_kwargs: Dictionary of keyword arguments
    """
    try:
        result = SchedulerService.create_job(job_data.dict())
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "job_id": result["job_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs", response_model=Dict)
async def get_all_jobs():
    """Get all scheduled jobs"""
    try:
        result = SchedulerService.get_all_jobs()
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "data": result["data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=Dict)
async def get_job(job_id: str):
    """Get a specific job by ID"""
    try:
        result = SchedulerService.get_job(job_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/jobs", response_model=Dict)
async def get_user_jobs(user_id: str):
    """Get all jobs for a specific user"""
    try:
        result = SchedulerService.get_jobs_by_user(user_id)
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "data": result["data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/jobs/{job_id}", response_model=Dict)
async def update_job(job_id: str, job_data: JobUpdateRequest):
    """Update a job"""
    try:
        result = SchedulerService.update_job(job_id, job_data.dict(exclude_none=True))
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "job_id": result["job_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/jobs/{job_id}", response_model=Dict)
async def delete_job(job_id: str):
    """Delete a job"""
    try:
        result = SchedulerService.delete_job(job_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "job_id": result["job_id"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/jobs/{job_id}/pause", response_model=Dict)
async def pause_job(job_id: str):
    """Pause a job"""
    try:
        result = SchedulerService.pause_job(job_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "job_id": result["job_id"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/jobs/{job_id}/resume", response_model=Dict)
async def resume_job(job_id: str):
    """Resume a paused job"""
    try:
        result = SchedulerService.resume_job(job_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "job_id": result["job_id"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jobs/{job_id}/run", response_model=Dict)
async def run_job_now(job_id: str):
    """Run a job immediately (create an execution)"""
    try:
        result = SchedulerService.run_job_now(job_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "execution_id": result["execution_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =================== Executions Endpoints ===================

@router.get("/executions", response_model=Dict)
async def get_executions(job_id: Optional[str] = Query(None)):
    """Get job executions"""
    try:
        result = SchedulerService.get_executions(job_id=job_id, limit=100)
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "data": result["data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/executions/{execution_id}", response_model=Dict)
async def get_execution(execution_id: str):
    """Get a specific execution by ID"""
    try:
        result = SchedulerService.get_execution(execution_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "data": result["data"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =================== Utility Endpoints ===================

@router.get("/available-jobs", response_model=Dict)
async def get_available_jobs_list():
    """Get all available job classes"""
    try:
        result = SchedulerService.get_available_jobs()
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "jobs": result["jobs"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats", response_model=Dict)
async def get_scheduler_stats(user_id: Optional[str] = Query(None)):
    """Get scheduler statistics"""
    try:
        result = SchedulerService.get_scheduler_stats(user_id=user_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "stats": result["stats"]
            }
        else:
            raise HTTPException(status_code=500, detail=result["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=Dict)
async def health_check():
    """Health check endpoint for scheduler"""
    try:
        result = SchedulerService.get_scheduler_stats()
        
        return {
            "status": "healthy" if result["success"] else "unhealthy",
            "message": "Scheduler is running",
            "timestamp": None
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
