"""User routes for API endpoints"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from schemas.user import UserIngestPayload, UserResponse
from services.user_service import UserService
from models.user import User
from typing import List, Dict

router = APIRouter(prefix="/api", tags=["users"])


@router.post("/single-user", response_model=Dict)
async def ingest_users_json(payload: UserIngestPayload):
    """
    API 1: Ingest users from JSON payload
    
    Expects JSON structure with users array containing:
    - user_name__v
    - user_first_name__v
    - user_last_name__v
    - user_email__v
    - user_timezone__v
    - user_locale__v
    - user_language__v
    - security_policy_id__v
    - file
    - vault_membership (array)
    - app_licensing (array)
    
    Stores email and name in MongoDB
    """
    try:
        # Initialize indexes if needed
        try:
            User.create_indexes()
        except:
            pass  # Indexes might already exist
        
        # Process the users
        result = UserService.create_users_from_json_payload(payload.dict())
        
        return {
            "status": "success" if result["failed"] == 0 else "partial",
            "message": f"Processed {result['total']} users. Success: {result['successful']}, Failed: {result['failed']}",
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/bulk-user")
async def ingest_users_excel(file: UploadFile = File(...)):
    """
    API 2: Ingest users from Excel file
    
    Expects Excel file with columns:
    - user_name__v
    - user_first_name__v
    - user_last_name__v
    - user_email__v
    - (and other optional columns)
    
    Reads row by row and creates users in MongoDB
    """
    try:
        # Validate file type
        if file.filename and not file.filename.endswith(('.xlsx', '.xls')):
            raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
        
        # Initialize indexes if needed
        try:
            User.create_indexes()
        except:
            pass  # Indexes might already exist
        
        # Read file content
        contents = await file.read()
        
        # Process the Excel file
        result = UserService.create_users_from_excel(contents)
        
        return {
            "status": "success" if result["failed"] == 0 else "partial",
            "message": f"Processed {result['total']} users. Success: {result['successful']}, Failed: {result['failed']}",
            "data": result
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all")
async def get_all_users():
    """Get all users from database"""
    try:
        users = UserService.get_all_users()
        return {
            "status": "success",
            "total": len(users),
            "data": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/{email}")
async def get_user_by_email(email: str):
    """Get user by email"""
    try:
        user = User.find_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "status": "success",
            "data": {
                "email": user.get("email"),
                "first_name": user.get("first_name"),
                "last_name": user.get("last_name"),
                "user_name": user.get("user_name"),
                "created_at": str(user.get("created_at")) if user.get("created_at") else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
