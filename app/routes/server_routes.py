"""Server routes for API endpoints"""
from fastapi import APIRouter, HTTPException
from schemas.server import ServerCreateRequest, ServerUpdateRequest, ServerResponse
from services.server_service import ServerService
from models.server import Server
from typing import List, Dict

router = APIRouter(prefix="/api/servers", tags=["servers"])


@router.post("/create", response_model=Dict)
async def create_server(server_data: ServerCreateRequest):
    """
    Create a new server for a user
    
    Expects:
    - user_id: The user ID who owns this server
    - name: Server name
    - hostname: Server hostname/IP address
    - port: Server port
    - status: Optional, defaults to "running"
    - connection_name: ServiceNow connection name (required)
    - instance_url: ServiceNow instance URL (required)
    - username: ServiceNow username (required)
    - password: ServiceNow password (required)
    """
    try:
        # Initialize indexes if needed
        try:
            Server.create_indexes()
        except:
            pass  # Indexes might already exist
        
        result = ServerService.create_server(server_data.dict())
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "server_id": result["server_id"]
            }
        else:
            raise HTTPException(status_code=400, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{server_id}", response_model=Dict)
async def get_server(server_id: str):
    """Get a server by ID"""
    try:
        result = ServerService.get_server(server_id)
        
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


@router.get("/user/{user_id}", response_model=Dict)
async def get_servers_by_user(user_id: str):
    """Get all servers for a specific user"""
    try:
        result = ServerService.get_servers_by_user(user_id)
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "data": result["data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=Dict)
async def get_all_servers():
    """Get all servers"""
    try:
        result = ServerService.get_all_servers()
        
        return {
            "status": "success",
            "message": result["message"],
            "total": result["total"],
            "data": result["data"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{server_id}", response_model=Dict)
async def update_server(server_id: str, update_data: ServerUpdateRequest):
    """
    Update a server
    
    Can update:
    - name
    - hostname
    - port
    - status
    - connection_name
    - instance_url
    - username
    - password
    """
    try:
        result = ServerService.update_server(server_id, update_data.dict(exclude_unset=True))
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"],
                "data": result.get("data")
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{server_id}", response_model=Dict)
async def delete_server(server_id: str):
    """Delete a server by ID"""
    try:
        result = ServerService.delete_server(server_id)
        
        if result["success"]:
            return {
                "status": "success",
                "message": result["message"]
            }
        else:
            raise HTTPException(status_code=404, detail=result["message"])
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/user/{user_id}", response_model=Dict)
async def delete_servers_by_user(user_id: str):
    """Delete all servers for a user"""
    try:
        result = ServerService.delete_servers_by_user(user_id)
        
        return {
            "status": "success",
            "message": result["message"],
            "deleted_count": result.get("deleted_count", 0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
