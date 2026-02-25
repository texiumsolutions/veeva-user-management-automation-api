# Quick Start Guide

## Setup (One-Time)

```bash
# 1. Navigate to project
cd d:\reactcheck\TexiumBackend

# 2. Install dependencies
python -m pip install -r requirements.txt

# 3. Ensure MongoDB is running
# MongoDB should be accessible at mongodb://localhost:27017
```

## Running the Application

### Start Server
```bash
python server.py
```

Output should show:
```
✓ Connected to MongoDB: texium_db
✓ Application started successfully
INFO:     Uvicorn running on http://0.0.0.0:5000
```

### Access API Documentation
Open browser and go to: `http://localhost:5000/docs`

## Common Tasks

### 1. Create Users from JSON

**File: test_json.py**
```python
import requests
import json

payload = {
    "users": [
        {
            "user_name__v": "john@example.com",
            "user_first_name__v": "John",
            "user_last_name__v": "Doe",
            "user_email__v": "john@example.com",
            "user_timezone__v": "America/New_York",
            "user_locale__v": "en_US",
            "user_language__v": "en",
            "security_policy_id__v": "123456",
            "file": "users.csv",
            "vault_membership": [],
            "app_licensing": []
        }
    ]
}

response = requests.post(
    "http://localhost:5000/api/users/ingest-json",
    json=payload
)

print(json.dumps(response.json(), indent=2))
```

Run: `python test_json.py`

### 2. Create Users from Excel

**File: test_excel.py**
```python
import requests

files = {'file': open('sample_users.xlsx', 'rb')}
response = requests.post(
    "http://localhost:5000/api/users/ingest-excel",
    files=files
)

print(response.json())
```

Run: `python test_excel.py`

### 3. Get All Users

```python
import requests

response = requests.get("http://localhost:5000/api/users/all")
print(response.json())
```

### 4. Search User by Email

```python
import requests

response = requests.get("http://localhost:5000/api/users/search/john@example.com")
print(response.json())
```

## Test All APIs

```bash
python test_apis.py
```

Expected Output:
```
============================================================
TEST SUMMARY
============================================================
JSON Ingestion API: ✓ PASSED
Get All Users: ✓ PASSED
Search User by Email: ✓ PASSED
Excel Ingestion API: ✓ PASSED

Total: 4/4 tests passed
```

## File Organization

✓ **models/** - User model (MongoDB operations)  
✓ **schemas/** - Pydantic validation schemas  
✓ **routes/** - API endpoints  
✓ **services/** - Business logic  
✓ **core/** - Database connection  
✓ **server.py** - Main application  

All files are in their proper locations!

## API Endpoints Quick Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/users/ingest-json` | Ingest users from JSON |
| POST | `/api/users/ingest-excel` | Ingest users from Excel |
| GET | `/api/users/all` | Get all users |
| GET | `/api/users/search/{email}` | Find user by email |
| GET | `/health` | Health check |

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## MongoDB Database

Database: `texium_db`  
Collection: `users`  

Connect with MongoDB client:
```
mongodb://localhost:27017/texium_db
```

---

**Status**: ✓ Everything is working and tested!
