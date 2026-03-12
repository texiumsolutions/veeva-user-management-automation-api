"""Connection routes - API endpoints for managing external system connections"""

from fastapi import APIRouter, HTTPException
from services.connection_service import ConnectionService
from schemas.connection import (
    ConnectionCreateRequest,
    ConnectionUpdateRequest,
    ConnectionListResponse,
    ConnectionDetailResponse,
    ConnectionActionResponse
)

router = APIRouter(
    prefix="/api/connections",
    tags=["Connections"]
)


@router.post(
    "/test",
    summary="Test external system connection"
)
def test_connection(payload: ConnectionCreateRequest):
    success = ConnectionService.test_connection(payload)

    if success:
        return {"status": "success", "message": "Connection successful"}

    return {"status": "failed", "message": "Connection failed"}


@router.post(
    "/create",
    response_model=ConnectionActionResponse,
    summary="Create a new connection"
)
def create_connection(payload: ConnectionCreateRequest):
    """
    Create a new external system connection.
    
    Supported systems:
    - Veeva Vault
    - ServiceNow
    - SAP LeanIX
    - Workday
    """
    return ConnectionService.create_connection(payload)


@router.get(
    "",
    response_model=ConnectionListResponse,
    summary="List all connections"
)
def list_connections():
    """
    Retrieve all configured system connections.
    """
    return ConnectionService.list_connections()


@router.get(
    "/{connection_id}",
    response_model=ConnectionDetailResponse,
    summary="Get connection by ID"
)
def get_connection(connection_id: str):
    """
    Retrieve a connection by MongoDB ObjectId.
    """
    return ConnectionService.get_connection(connection_id)


@router.get(
    "/name/{connection_name}",
    response_model=ConnectionDetailResponse,
    summary="Get connection by name"
)
def get_connection_by_name(connection_name: str):
    """
    Retrieve a connection using its unique connectionName.
    """
    return ConnectionService.get_connection_by_name(connection_name)


@router.patch(
    "/{connection_id}",
    response_model=ConnectionActionResponse,
    summary="Update connection"
)
def update_connection(connection_id: str, payload: ConnectionUpdateRequest):
    """
    Update connection configuration.
    """
    return ConnectionService.update_connection(connection_id, payload)


@router.delete(
    "/{connection_id}",
    response_model=ConnectionActionResponse,
    summary="Delete connection"
)
def delete_connection(connection_id: str):
    """
    Delete a connection permanently.
    """
    return ConnectionService.delete_connection(connection_id)