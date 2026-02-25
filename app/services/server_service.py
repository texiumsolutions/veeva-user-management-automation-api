"""Server service for business logic"""
from models.server import Server
from pymongo.errors import DuplicateKeyError
from typing import List, Dict, Optional


class ServerService:
    """Service for server operations"""
    
    @staticmethod
    def create_server(server_data: dict) -> Dict:
        """
        Create a new server for a user
        """
        try:
            # Validate required fields
            required_fields = ["user_id", "name", "hostname", "port"]
            for field in required_fields:
                if not server_data.get(field):
                    return {
                        "success": False,
                        "message": f"Missing required field: {field}",
                        "server_id": None
                    }
            
            server_id = Server.insert_server(server_data)
            return {
                "success": True,
                "message": f"Server {server_data.get('name')} created successfully",
                "server_id": str(server_id)
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "server_id": None
            }
    
    @staticmethod
    def get_server(server_id: str) -> Dict:
        """
        Get a server by ID
        """
        try:
            server = Server.find_server_by_id(server_id)
            if not server:
                return {
                    "success": False,
                    "message": "Server not found",
                    "data": None
                }
            
            return {
                "success": True,
                "message": "Server retrieved successfully",
                "data": {
                    "id": str(server.get("_id")),
                    "user_id": str(server.get("user_id")),
                    "name": server.get("name"),
                    "hostname": server.get("hostname"),
                    "port": server.get("port"),
                    "status": server.get("status"),
                    "connection_name": server.get("connection_name"),
                    "instance_url": server.get("instance_url"),
                    "username": server.get("username"),
                    "password": server.get("password"),
                    "created_at": str(server.get("created_at")) if server.get("created_at") else None,
                    "updated_at": str(server.get("updated_at")) if server.get("updated_at") else None
                }
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "data": None
            }
    
    @staticmethod
    def get_servers_by_user(user_id: str) -> Dict:
        """
        Get all servers for a user
        """
        try:
            servers = Server.find_servers_by_user(user_id)
            
            server_list = []
            for server in servers:
                server_list.append({
                    "id": str(server.get("_id")),
                    "user_id": str(server.get("user_id")),
                    "name": server.get("name"),
                    "hostname": server.get("hostname"),
                    "port": server.get("port"),
                    "status": server.get("status"),
                    "connection_name": server.get("connection_name"),
                    "instance_url": server.get("instance_url"),
                    "username": server.get("username"),
                    "password": server.get("password"),
                    "created_at": str(server.get("created_at")) if server.get("created_at") else None,
                    "updated_at": str(server.get("updated_at")) if server.get("updated_at") else None
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(servers)} servers",
                "total": len(servers),
                "data": server_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": []
            }
    
    @staticmethod
    def get_all_servers() -> Dict:
        """
        Get all servers
        """
        try:
            servers = Server.find_all_servers()
            
            server_list = []
            for server in servers:
                server_list.append({
                    "id": str(server.get("_id")),
                    "user_id": str(server.get("user_id")),
                    "name": server.get("name"),
                    "hostname": server.get("hostname"),
                    "port": server.get("port"),
                    "status": server.get("status"),
                    "connection_name": server.get("connection_name"),
                    "instance_url": server.get("instance_url"),
                    "username": server.get("username"),
                    "password": server.get("password"),
                    "created_at": str(server.get("created_at")) if server.get("created_at") else None,
                    "updated_at": str(server.get("updated_at")) if server.get("updated_at") else None
                })
            
            return {
                "success": True,
                "message": f"Retrieved {len(servers)} servers",
                "total": len(servers),
                "data": server_list
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "total": 0,
                "data": []
            }
    
    @staticmethod
    def update_server(server_id: str, update_data: dict) -> Dict:
        """
        Update a server
        """
        try:
            # First, verify the server exists
            server = Server.find_server_by_id(server_id)
            if not server:
                return {
                    "success": False,
                    "message": "Server not found"
                }
            
            # Update only provided fields
            update_dict = {}
            if update_data.get("name"):
                update_dict["name"] = update_data.get("name")
            if update_data.get("hostname"):
                update_dict["hostname"] = update_data.get("hostname")
            if update_data.get("port"):
                update_dict["port"] = update_data.get("port")
            if update_data.get("status"):
                update_dict["status"] = update_data.get("status")
            if update_data.get("connection_name"):
                update_dict["connection_name"] = update_data.get("connection_name")
            if update_data.get("instance_url"):
                update_dict["instance_url"] = update_data.get("instance_url")
            if update_data.get("username"):
                update_dict["username"] = update_data.get("username")
            if update_data.get("password"):
                update_dict["password"] = update_data.get("password")
            
            if not update_dict:
                return {
                    "success": False,
                    "message": "No fields to update"
                }
            
            success = Server.update_server(server_id, update_dict)
            
            if success:
                # Return updated server
                updated_server = Server.find_server_by_id(server_id)
                return {
                    "success": True,
                    "message": "Server updated successfully",
                    "data": {
                        "id": str(updated_server.get("_id")),
                        "user_id": str(updated_server.get("user_id")),
                        "name": updated_server.get("name"),
                        "hostname": updated_server.get("hostname"),
                        "port": updated_server.get("port"),
                        "status": updated_server.get("status"),
                        "connection_name": updated_server.get("connection_name"),
                        "instance_url": updated_server.get("instance_url"),
                        "username": updated_server.get("username"),
                        "password": updated_server.get("password"),
                        "created_at": str(updated_server.get("created_at")) if updated_server.get("created_at") else None,
                        "updated_at": str(updated_server.get("updated_at")) if updated_server.get("updated_at") else None
                    }
                }
            else:
                return {
                    "success": False,
                    "message": "Failed to update server"
                }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def delete_server(server_id: str) -> Dict:
        """
        Delete a server
        """
        try:
            success = Server.delete_server(server_id)
            
            if success:
                return {
                    "success": True,
                    "message": "Server deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "message": "Server not found or failed to delete"
                }
        except Exception as e:
            return {
                "success": False,
                "message": str(e)
            }
    
    @staticmethod
    def delete_servers_by_user(user_id: str) -> Dict:
        """
        Delete all servers for a user
        """
        try:
            count = Server.delete_servers_by_user(user_id)
            return {
                "success": True,
                "message": f"Deleted {count} servers",
                "deleted_count": count
            }
        except Exception as e:
            return {
                "success": False,
                "message": str(e),
                "deleted_count": 0
            }
