"""
Hourly Scheduler Routes
Separate router for hourly scheduling endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
from services.scheduler_service import SchedulerService

router = APIRouter(
    prefix="/api/scheduler",
    tags=["scheduler-hourly"]
)


@router.post("/jobs/{job_id}/schedule-hourly/{minute}", response_model=Dict)
async def schedule_job_hourly(job_id: str, minute: int):
    """
    Schedule a job to run every hour at a specific minute.
    
    Example:
        POST /api/scheduler/jobs/123/schedule-hourly/15
        → Runs every hour at minute 15 (15 * * * *)
    """

    try:
        # Validate minute range
        if minute < 0 or minute > 59:
            raise HTTPException(
                status_code=400,
                detail="Minute must be between 0 and 59"
            )

        cron_config = {
            "minute": str(minute),
            "hour": "*",
            "day_of_month": "*",
            "month": "*",
            "day_of_week": "*",
        }

        result = SchedulerService.update_job(job_id, cron_config)

        if result.get("success"):
            return {
                "status": "success",
                "message": f"Job scheduled every hour at minute {minute}",
                "job_id": job_id,
                "cron": f"{minute} * * * *"
            }
        else:
            raise HTTPException(
                status_code=400,
                detail=result.get("message", "Failed to update job")
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))