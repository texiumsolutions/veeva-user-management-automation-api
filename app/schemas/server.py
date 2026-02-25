"""Pydantic schemas for server validation"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ServerCreateRequest(BaseModel):
    """Schema for server creation request"""
    user_id: str
    name: str
    hostname: str
    port: int
    status: Optional[str] = "running"
    connection_name: str
    instance_url: str
    username: str
    password: str


class ServerUpdateRequest(BaseModel):
    """Schema for server update request"""
    name: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    status: Optional[str] = None
    connection_name: Optional[str] = None
    instance_url: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class ServerResponse(BaseModel):
    """Schema for server response"""
    id: str
    user_id: str
    nonnection_name: str
    instance_url: str
    username: str
    password: str
    came: str
    hostname: str
    port: int
    status: str
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class ServerListResponse(BaseModel):
    """Schema for server list response"""
    servers: List[ServerResponse]
    total: int
