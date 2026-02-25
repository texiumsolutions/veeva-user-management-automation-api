"""Pydantic schemas for validation"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional


class VaultMembershipSchema(BaseModel):
    """Schema for vault membership"""
    vault_id: str
    vault_name: str
    vault_type: str
    role__v: str
    status__v: str
    license_type__v: str


class AppLicensingSchema(BaseModel):
    """Schema for app licensing"""
    vault_id: str
    application: str
    licensed: bool


class UserIngestSchema(BaseModel):
    """Schema for ingesting user from JSON"""
    user_name__v: str
    user_first_name__v: str
    user_last_name__v: str
    user_email__v: EmailStr
    user_timezone__v: str
    user_locale__v: str
    user_language__v: str
    security_policy_id__v: str
    file: str
    vault_membership: List[VaultMembershipSchema]
    app_licensing: List[AppLicensingSchema]


class UserIngestPayload(BaseModel):
    """Schema for the complete ingestion payload"""
    users: List[UserIngestSchema]


class UserCreateRequest(BaseModel):
    """Schema for user creation request from Excel"""
    email: str
    first_name: str
    last_name: str
    user_name: Optional[str] = None


class UserResponse(BaseModel):
    """Schema for user response"""
    email: str
    first_name: str
    last_name: str
    user_name: str
    created_at: Optional[str] = None
