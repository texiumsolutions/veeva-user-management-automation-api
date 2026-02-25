"""Schemas for scheduler API requests and responses"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime


class JobCreateRequest(BaseModel):
    """Request schema for creating a new job"""
    user_id: str
    job_class_string: str
    name: str
    description: Optional[str] = None
    pub_args: Optional[List] = []
    pub_kwargs: Optional[Dict] = {}
    minute: Optional[str] = "*"
    hour: Optional[str] = "*"
    day_of_month: Optional[str] = "*"
    month: Optional[str] = "*"
    day_of_week: Optional[str] = "*"
    week: Optional[str] = "*"


class JobUpdateRequest(BaseModel):
    """Request schema for updating a job"""
    name: Optional[str] = None
    description: Optional[str] = None
    pub_args: Optional[List] = None
    pub_kwargs: Optional[Dict] = None
    minute: Optional[str] = None
    hour: Optional[str] = None
    day_of_month: Optional[str] = None
    month: Optional[str] = None
    day_of_week: Optional[str] = None
    week: Optional[str] = None
    is_enabled: Optional[bool] = None


class JobResponse(BaseModel):
    """Response schema for a job"""
    job_id: str = Field(..., alias="_id")
    user_id: str
    job_class_string: str
    name: str
    description: str
    pub_args: List
    pub_kwargs: Dict
    minute: str
    hour: str
    day_of_month: str
    month: str
    day_of_week: str
    week: str
    is_enabled: bool
    is_paused: bool
    created_at: datetime
    updated_at: datetime
    last_run_time: Optional[datetime] = None
    next_run_time: Optional[datetime] = None
    total_executions: int


class JobExecutionResponse(BaseModel):
    """Response schema for a job execution"""
    execution_id: str = Field(..., alias="_id")
    job_id: str
    user_id: str
    job_name: str
    job_class_string: str
    status: str
    output: str
    error: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    created_at: datetime


class JobListResponse(BaseModel):
    """Response schema for listing jobs"""
    status: str
    message: str
    total: int
    data: List[Dict]


class JobDetailResponse(BaseModel):
    """Response schema for job details"""
    status: str
    message: str
    data: Dict


class ExecutionListResponse(BaseModel):
    """Response schema for listing executions"""
    status: str
    message: str
    total: int
    data: List[Dict]


class ExecutionDetailResponse(BaseModel):
    """Response schema for execution details"""
    status: str
    message: str
    data: Dict


class JobActionResponse(BaseModel):
    """Response schema for job actions (create, delete, pause, resume)"""
    status: str
    message: str
    job_id: Optional[str] = None
    execution_id: Optional[str] = None


class ExecutionRunResponse(BaseModel):
    """Response schema for running a job"""
    status: str
    message: str
    execution_id: str


class AvailableJobsResponse(BaseModel):
    """Response schema for available job classes"""
    status: str
    message: str
    jobs: List[Dict]


class JobStatsResponse(BaseModel):
    """Response schema for job statistics"""
    status: str
    message: str
    total_jobs: int
    enabled_jobs: int
    paused_jobs: int
    total_executions: int
    completed_executions: int
    failed_executions: int
