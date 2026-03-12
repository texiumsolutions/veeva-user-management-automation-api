"""Connection service - business logic for connections"""

from models.connection import Connection
from fastapi import HTTPException
from bson import ObjectId
import requests


class ConnectionService:

    @staticmethod
    def test_connection(connection):
        connection_dict=connection.model_dump()

        connection_type = connection_dict.get("type")
        print("here done type")

        if connection_type == "veeva_vault":
            return ConnectionService._test_veeva(connection_dict)

        elif connection_type == "servicenow":
            return ConnectionService._test_servicenow(connection_dict)

        elif connection_type == "workday":
            return ConnectionService._test_workday(connection_dict)

        elif connection_type == "successfactors":
            return ConnectionService._test_successfactors(connection_dict)

        elif connection_type == "cornerstone":
            return ConnectionService._test_cornerstone(connection_dict)

        else:
            raise Exception("Unsupported connection type")

    # -------------------------
    # VEEVA
    # -------------------------

    @staticmethod
    def _test_veeva(connection):

        try:
            config = connection["config"]
            credentials = connection["credentials"]

            instance_url = config.get("instanceUrl")
            api_version = config.get("apiVersion", "v23.2")

            if not instance_url:
                return False

            url = f"{instance_url}/api/{api_version}/objects/documents?limit=1"

            response = requests.get(
                url,
                auth=(credentials.get("username"), credentials.get("password")),
                timeout=10
            )

            return response.status_code == 200

        except requests.exceptions.RequestException as e:
            print("Veeva connection error:", str(e))
            return False


    # -------------------------
    # SERVICENOW
    # -------------------------

    @staticmethod
    def _test_servicenow(connection):

        try:
            config = connection["config"]
            credentials = connection["credentials"]

            instance_url = config.get("instanceUrl")

            if not instance_url:
                return False

            url = f"{instance_url}/api/now/table/sys_user?sysparm_limit=1"

            response = requests.get(
                url,
                auth=(credentials.get("username"), credentials.get("password")),
                headers={"Accept": "application/json"},
                timeout=10
            )

            return response.status_code == 200

        except requests.exceptions.RequestException as e:
            print("ServiceNow connection error:", str(e))
            return False


    # -------------------------
    # WORKDAY
    # -------------------------

    @staticmethod
    def _test_workday(connection):

        try:
            config = connection["config"]
            credentials = connection["credentials"]

            base_url = config.get("baseUrl")
            tenant = config.get("tenant")

            if not base_url or not tenant:
                return False

            url = f"{base_url}/ccx/api/v1/{tenant}/workers?limit=1"

            response = requests.get(
                url,
                auth=(credentials.get("clientId"), credentials.get("clientSecret")),
                timeout=10
            )

            return response.status_code in [200, 401]

        except requests.exceptions.RequestException as e:
            print("Workday connection error:", str(e))
            return False


    # -------------------------
    # SUCCESSFACTORS
    # -------------------------

    @staticmethod
    def _test_successfactors(connection):

        try:
            config = connection["config"]
            credentials = connection["credentials"]

            base_url = config.get("baseUrl")
            company_id = config.get("companyId")

            username = credentials.get("username")
            password = credentials.get("password")

            if not base_url or not username or not password:
                return False

            auth_user = f"{username}@{company_id}"

            url = f"{base_url}/odata/v2/User?$top=1&$format=json"

            response = requests.get(
                url,
                auth=(auth_user, password),
                headers={"Accept": "application/json"},
                timeout=10
            )

            return response.status_code == 200

        except requests.exceptions.RequestException as e:
            print("SuccessFactors connection error:", str(e))
            return False


    # -------------------------
    # CORNERSTONE
    # -------------------------

    @staticmethod
    def _test_cornerstone(connection):

        try:
            config = connection["config"]
            credentials = connection["credentials"]

            base_url = config.get("baseUrl")

            client_id = credentials.get("clientId")
            client_secret = credentials.get("clientSecret")

            if not base_url or not client_id or not client_secret:
                return False

            url = f"{base_url}/services/api/x/users/v1"

            response = requests.get(
                url,
                auth=(client_id, client_secret),
                timeout=10
            )

            return response.status_code in [200, 401]

        except requests.exceptions.RequestException as e:
            print("Cornerstone connection error:", str(e))
            return False

    @staticmethod
    def create_connection(payload):

        connection_id = Connection.insert_connection(payload.model_dump())

        return {
            "status": "success",
            "message": "Connection created successfully",
            "connection_id": str(connection_id)
        }

    @staticmethod
    def list_connections():

        connections = Connection.find_all_connections()

        data = []
        for conn in connections:
            conn["_id"] = str(conn["_id"])
            conn.pop("credentials", None)
            data.append(conn)

        return {
            "status": "success",
            "message": "Connections retrieved successfully",
            "total": len(data),
            "data": data
        }

    @staticmethod
    def get_connection(connection_id: str):

        connection = Connection.find_connection_by_id(connection_id)

        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")

        connection["_id"] = str(connection["_id"])
        connection.pop("credentials", None)

        return {
            "status": "success",
            "message": "Connection retrieved successfully",
            "data": connection
        }

    @staticmethod
    def get_connection_by_name(connection_name: str):

        connection = Connection.find_connection_by_name(connection_name)

        if not connection:
            raise HTTPException(status_code=404, detail="Connection not found")

        connection["_id"] = str(connection["_id"])
        connection.pop("credentials", None)

        return {
            "status": "success",
            "message": "Connection retrieved successfully",
            "data": connection
        }

    @staticmethod
    def update_connection(connection_id: str, payload):

        updated = Connection.update_connection(connection_id, payload.model_dump(exclude_none=True))

        if not updated:
            raise HTTPException(status_code=404, detail="Connection not found or not updated")

        return {
            "status": "success",
            "message": "Connection updated successfully",
            "connection_id": connection_id
        }

    @staticmethod
    def delete_connection(connection_id: str):

        deleted = Connection.delete_connection(connection_id)

        if not deleted:
            raise HTTPException(status_code=404, detail="Connection not found")

        return {
            "status": "success",
            "message": "Connection deleted successfully",
            "connection_id": connection_id
        }