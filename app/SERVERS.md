# Server Management - CRUD Operations Guide

## Overview

The Server CRUD API allows you to manage servers associated with users. Each server belongs to a specific user and contains information such as hostname, port, name, and status.

## Server Model Structure

```json
{
  "id": "60d5ec49c1234abcd5678901",
  "user_id": "60d5ec49c1234abcd5678900",
  "name": "Production Server",
  "hostname": "192.168.1.100",
  "port": 8080,
  "status": "running",
  "created_at": "2024-02-22T10:30:00",
  "updated_at": "2024-02-22T10:30:00"
}
```

## API Endpoints

### 1. Create Server (POST)
**Endpoint:** `POST /api/servers/create`

Creates a new server for a user.

**Request Body:**
```json
{
  "user_id": "60d5ec49c1234abcd5678900",
  "name": "Production Server",
  "hostname": "192.168.1.100",
  "port": 8080,
  "status": "running"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Server Production Server created successfully",
  "server_id": "60d5ec49c1234abcd5678901"
}
```

**Example using Python:**
```python
import requests

url = "http://localhost:5000/api/servers/create"

server_data = {
    "user_id": "60d5ec49c1234abcd5678900",
    "name": "Web Server 1",
    "hostname": "web1.example.com",
    "port": 80,
    "status": "running"
}

response = requests.post(url, json=server_data)
print(response.json())
```

---

### 2. Get Server by ID (GET)
**Endpoint:** `GET /api/servers/{server_id}`

Retrieves a specific server by its ID.

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Server retrieved successfully",
  "data": {
    "id": "60d5ec49c1234abcd5678901",
    "user_id": "60d5ec49c1234abcd5678900",
    "name": "Production Server",
    "hostname": "192.168.1.100",
    "port": 8080,
    "status": "running",
    "created_at": "2024-02-22T10:30:00",
    "updated_at": "2024-02-22T10:30:00"
  }
}
```

**Example using Python:**
```python
import requests

server_id = "60d5ec49c1234abcd5678901"
url = f"http://localhost:5000/api/servers/{server_id}"

response = requests.get(url)
print(response.json())
```

---

### 3. Get All Servers for a User (GET)
**Endpoint:** `GET /api/servers/user/{user_id}`

Retrieves all servers belonging to a specific user.

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Retrieved 3 servers",
  "total": 3,
  "data": [
    {
      "id": "60d5ec49c1234abcd5678901",
      "user_id": "60d5ec49c1234abcd5678900",
      "name": "Production Server",
      "hostname": "192.168.1.100",
      "port": 8080,
      "status": "running",
      "created_at": "2024-02-22T10:30:00",
      "updated_at": "2024-02-22T10:30:00"
    },
    {
      "id": "60d5ec49c1234abcd5678902",
      "user_id": "60d5ec49c1234abcd5678900",
      "name": "Dev Server",
      "hostname": "192.168.1.101",
      "port": 8081,
      "status": "running",
      "created_at": "2024-02-22T11:00:00",
      "updated_at": "2024-02-22T11:00:00"
    }
  ]
}
```

**Example using Python:**
```python
import requests

user_id = "60d5ec49c1234abcd5678900"
url = f"http://localhost:5000/api/servers/user/{user_id}"

response = requests.get(url)
result = response.json()
print(f"User has {result['total']} servers")
for server in result['data']:
    print(f"  - {server['name']}: {server['hostname']}:{server['port']}")
```

---

### 4. Get All Servers (GET)
**Endpoint:** `GET /api/servers/`

Retrieves all servers in the system.

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Retrieved 5 servers",
  "total": 5,
  "data": [
    {
      "id": "60d5ec49c1234abcd5678901",
      "user_id": "60d5ec49c1234abcd5678900",
      "name": "Production Server",
      "hostname": "192.168.1.100",
      "port": 8080,
      "status": "running",
      "created_at": "2024-02-22T10:30:00",
      "updated_at": "2024-02-22T10:30:00"
    }
  ]
}
```

**Example using Python:**
```python
import requests

url = "http://localhost:5000/api/servers/"

response = requests.get(url)
result = response.json()
print(f"Total servers in system: {result['total']}")
```

---

### 5. Update Server (PUT)
**Endpoint:** `PUT /api/servers/{server_id}`

Updates one or more fields of a server. Only provide fields you want to update.

**Request Body (all fields optional):**
```json
{
  "name": "Production Server Updated",
  "hostname": "192.168.1.105",
  "port": 8085,
  "status": "stopped"
}
```

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Server updated successfully",
  "data": {
    "id": "60d5ec49c1234abcd5678901",
    "user_id": "60d5ec49c1234abcd5678900",
    "name": "Production Server Updated",
    "hostname": "192.168.1.105",
    "port": 8085,
    "status": "stopped",
    "created_at": "2024-02-22T10:30:00",
    "updated_at": "2024-02-22T12:00:00"
  }
}
```

**Example using Python:**
```python
import requests

server_id = "60d5ec49c1234abcd5678901"
url = f"http://localhost:5000/api/servers/{server_id}"

update_data = {
    "status": "stopped",
    "hostname": "192.168.1.105"
}

response = requests.put(url, json=update_data)
print(response.json())
```

---

### 6. Delete Server (DELETE)
**Endpoint:** `DELETE /api/servers/{server_id}`

Deletes a specific server by its ID.

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Server deleted successfully"
}
```

**Example using Python:**
```python
import requests

server_id = "60d5ec49c1234abcd5678901"
url = f"http://localhost:5000/api/servers/{server_id}"

response = requests.delete(url)
print(response.json())
```

---

### 7. Delete All Servers for a User (DELETE)
**Endpoint:** `DELETE /api/servers/user/{user_id}`

Deletes all servers belonging to a specific user.

**Response (Success - 200):**
```json
{
  "status": "success",
  "message": "Deleted 3 servers",
  "deleted_count": 3
}
```

**Example using Python:**
```python
import requests

user_id = "60d5ec49c1234abcd5678900"
url = f"http://localhost:5000/api/servers/user/{user_id}"

response = requests.delete(url)
result = response.json()
print(f"Deleted {result['deleted_count']} servers")
```

---

## Testing the APIs

### Using cURL

**Create Server:**
```bash
curl -X POST "http://localhost:5000/api/servers/create" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "60d5ec49c1234abcd5678900",
    "name": "API Test Server",
    "hostname": "test.example.com",
    "port": 3000,
    "status": "running"
  }'
```

**Get All Servers:**
```bash
curl -X GET "http://localhost:5000/api/servers/"
```

**Get User Servers:**
```bash
curl -X GET "http://localhost:5000/api/servers/user/60d5ec49c1234abcd5678900"
```

**Update Server:**
```bash
curl -X PUT "http://localhost:5000/api/servers/60d5ec49c1234abcd5678901" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "maintenance"
  }'
```

**Delete Server:**
```bash
curl -X DELETE "http://localhost:5000/api/servers/60d5ec49c1234abcd5678901"
```

---

### Using Swagger UI

1. Start the server: `python server.py`
2. Open browser: `http://localhost:5000/docs`
3. Look for "servers" section in the Swagger interface
4. Try out all endpoints directly from the browser

---

## Status Values

Common server status values:
- `running` - Server is currently running
- `stopped` - Server is stopped
- `maintenance` - Server is under maintenance
- `error` - Server has encountered an error

You can use any string value for status, but it's recommended to stick to standardized values.

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Server not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Missing required field: hostname"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred"
}
```

---

## Complete Example: Create, List, Update, Delete

```python
import requests
import json

BASE_URL = "http://localhost:5000/api/servers"

# Step 1: Create a server
print("1. Creating a server...")
user_id = "60d5ec49c1234abcd5678900"
server_data = {
    "user_id": user_id,
    "name": "My Test Server",
    "hostname": "192.168.1.50",
    "port": 5000,
    "status": "running"
}
response = requests.post(f"{BASE_URL}/create", json=server_data)
server_id = response.json()["server_id"]
print(f"   Server created with ID: {server_id}")

# Step 2: Get the server
print("\n2. Retrieving the server...")
response = requests.get(f"{BASE_URL}/{server_id}")
server = response.json()["data"]
print(f"   Server: {server['name']} at {server['hostname']}:{server['port']}")

# Step 3: Get all servers for user
print("\n3. Getting all servers for user...")
response = requests.get(f"{BASE_URL}/user/{user_id}")
servers = response.json()["data"]
print(f"   User has {len(servers)} server(s)")

# Step 4: Update the server
print("\n4. Updating the server...")
update_data = {
    "status": "maintenance",
    "hostname": "192.168.1.51"
}
response = requests.put(f"{BASE_URL}/{server_id}", json=update_data)
print(f"   Server updated: new status = maintenance")

# Step 5: Delete the server
print("\n5. Deleting the server...")
response = requests.delete(f"{BASE_URL}/{server_id}")
print(f"   Server deleted successfully")

print("\n✓ All operations completed successfully!")
```

---

## Database Structure

Servers are stored in MongoDB with the following structure:

```javascript
{
  _id: ObjectId,
  user_id: ObjectId,     // Reference to user
  name: string,
  hostname: string,
  port: number,
  status: string,
  created_at: datetime,
  updated_at: datetime
}
```

**Indexes Created:**
- `user_id` - For efficient queries by user
- `name` - For searching servers by name
- `hostname` - For searching servers by hostname
