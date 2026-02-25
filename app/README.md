# Texium User Management API

A FastAPI-based REST API for managing users with MongoDB storage. Supports ingesting users from JSON and Excel files.

## Features

- **JSON Ingestion API**: Ingest user data from structured JSON payloads
- **Excel Ingestion API**: Read users from Excel files (row by row)
- **User Search**: Find users by email
- **User Listing**: Retrieve all users from the database
- **MongoDB Integration**: Persistent storage with email and user name fields
- **Error Handling**: Comprehensive error responses and duplicate detection

## Requirements

- Python 3.9+
- MongoDB (running on localhost:27017 by default)
- All dependencies listed in requirements.txt

## Installation & Setup

### 1. Install Dependencies

```bash
cd d:\reactcheck\TexiumBackend
python -m pip install -r requirements.txt
```

### 2. Configure MongoDB Connection

The `.env` file contains MongoDB configuration:

```env
PORT=5000
DEBUG=true
MONGO_URI=mongodb://localhost:27017
DB_NAME=texium_db
```

Update these values if your MongoDB server is on a different host or port.

### 3. Start the Server

```bash
python server.py
```

The server will:
- Connect to MongoDB
- Start listening on `http://localhost:5000`
- Display auto-generated API documentation at `http://localhost:5000/docs`

## API Endpoints

### 1. Health Check
```
GET /health
GET /
```
Returns server health status.

**Example Response:**
```json
{
  "status": "healthy",
  "service": "Texium API"
}
```

---

### 2. Ingest Users from JSON
```
POST /api/users/ingest-json
```

Ingest user data from a JSON payload. The JSON must follow the specified structure with users array containing nested vault_membership and app_licensing arrays.

**Request Body:**
```json
{
  "users": [
    {
      "user_name__v": "jsmith@example.com",
      "user_first_name__v": "Par",
      "user_last_name__v": "Smith",
      "user_email__v": "jsmith@example.com",
      "user_timezone__v": "America/New_York",
      "user_locale__v": "en_US",
      "user_language__v": "en",
      "security_policy_id__v": "1234567890123",
      "file": "users.csv",
      "vault_membership": [
        {
          "vault_id": "1001",
          "vault_name": "Clinical Vault",
          "vault_type": "clinical",
          "role__v": "vault_owner__v",
          "status__v": "active__v",
          "license_type__v": "full_user__v"
        }
      ],
      "app_licensing": [
        {
          "vault_id": "1001",
          "application": "clinical_operations__v",
          "licensed": true
        }
      ]
    }
  ]
}
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Processed 1 users. Success: 1, Failed: 0",
  "data": {
    "total": 1,
    "successful": 1,
    "failed": 0,
    "details": [
      {
        "success": true,
        "message": "User jsmith@example.com created successfully",
        "user_id": "507f1f77bcf86cd799439011"
      }
    ]
  }
}
```

**Notes:**
- Only email and name fields are stored in MongoDB
- Duplicate emails are detected and handled gracefully
- vault_membership and app_licensing data is included in the request but currently stored for reference

---

### 3. Ingest Users from Excel
```
POST /api/users/ingest-excel
```

Upload an Excel file (.xlsx or .xls) to create users from rows. The file should have the following columns:

**Required Columns:**
- `user_email__v` - User's email address
- `user_first_name__v` - First name
- `user_last_name__v` - Last name
- `user_name__v` - Username (optional, defaults to email)

**Optional Columns:**
- `user_timezone__v`
- `user_locale__v`
- `user_language__v`
- `security_policy_id__v`
- `file`

**Example Request (using curl):**
```bash
curl -X POST http://localhost:5000/api/users/ingest-excel \
  -F "file=@sample_users.xlsx"
```

**Response (Success):**
```json
{
  "status": "success",
  "message": "Processed 5 users. Success: 5, Failed: 0",
  "data": {
    "total": 5,
    "successful": 5,
    "failed": 0,
    "details": [
      {
        "row": 2,
        "success": true,
        "message": "User jim@veevapharm.com created successfully",
        "user_id": "507f1f77bcf86cd799439011"
      }
    ]
  }
}
```

**Notes:**
- Reads data row by row, starting from row 2 (row 1 is headers)
- Empty rows are skipped
- Each row's result is included in the details array with its row number

---

### 4. Get All Users
```
GET /api/users/all
```

Retrieve all users from the database.

**Response:**
```json
{
  "status": "success",
  "total": 10,
  "data": [
    {
      "email": "user1@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "user_name": "user1@example.com",
      "created_at": "2026-02-21T18:16:58.858000"
    },
    {
      "email": "user2@example.com",
      "first_name": "Jane",
      "last_name": "Smith",
      "user_name": "user2@example.com",
      "created_at": "2026-02-21T18:17:06.046000"
    }
  ]
}
```

---

### 5. Search User by Email
```
GET /api/users/search/{email}
```

Find a specific user by their email address.

**Example:**
```
GET /api/users/search/jsmith@example.com
```

**Response (Found):**
```json
{
  "status": "success",
  "data": {
    "email": "jsmith@example.com",
    "first_name": "Par",
    "last_name": "Smith",
    "user_name": "jsmith@example.com",
    "created_at": "2026-02-21T18:16:58.858000"
  }
}
```

**Response (Not Found):**
```json
{
  "detail": "User not found"
}
```
Status Code: 404

---

## Database Schema

### Users Collection

```javascript
{
  "_id": ObjectId,
  "email": String (unique),
  "first_name": String,
  "last_name": String,
  "user_name": String (unique),
  "created_at": DateTime
}
```

**Indexes:**
- `email` (unique)
- `user_name` (unique)

---

## Testing

### Run All Tests

```bash
python test_apis.py
```

This script tests:
1. JSON ingestion API
2. Getting all users
3. Searching users by email
4. Excel ingestion API

### Create Sample Excel File

```bash
python create_sample_excel.py
```

This generates `sample_users.xlsx` with sample user data for testing.

### Manual Testing with curl

**Test JSON Ingestion:**
```bash
curl -X POST http://localhost:5000/api/users/ingest-json \
  -H "Content-Type: application/json" \
  -d @payload.json
```

**Test Excel Ingestion:**
```bash
curl -X POST http://localhost:5000/api/users/ingest-excel \
  -F "file=@sample_users.xlsx"
```

**Get All Users:**
```bash
curl http://localhost:5000/api/users/all
```

**Search User:**
```bash
curl http://localhost:5000/api/users/search/jsmith@example.com
```

---

## Project Structure

```
TexiumBackend/
├── server.py                  # Main FastAPI application
├── requirements.txt           # Python dependencies
├── .env                       # Configuration (MongoDB URI, port, etc.)
├── test_apis.py              # API test suite
├── create_sample_excel.py    # Sample Excel file generator
├── core/
│   └── database.py           # MongoDB connection and initialization
├── models/
│   └── user.py               # User model with database operations
├── schemas/
│   └── user.py               # Pydantic validation schemas
├── routes/
│   └── user_routes.py        # API endpoint definitions
└── services/
    └── user_service.py       # Business logic for user operations
```

---

## Error Handling

### Duplicate Email
If attempting to create a user with an existing email:

**Response:**
```json
{
  "detail": "User with email user@example.com already exists"
}
```

### Invalid File Type (Excel)
If uploading a non-Excel file:

**Response:**
```json
{
  "detail": "File must be an Excel file (.xlsx or .xls)"
}
```

### MongoDB Connection Error
If MongoDB is not accessible, the server will not start:

```
✗ Failed to connect to MongoDB. Make sure MongoDB is running.
```

Ensure MongoDB is running before starting the application.

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| PORT | 5000 | Server port |
| DEBUG | true | Debug mode |
| MONGO_URI | mongodb://localhost:27017 | MongoDB connection string |
| DB_NAME | texium_db | Database name |

---

## API Documentation

Once the server is running, interactive API documentation is available at:

- **Swagger UI**: http://localhost:5000/docs
- **ReDoc**: http://localhost:5000/redoc

You can test all endpoints directly from the documentation interface.

---

## Troubleshooting

### MongoDB Connection Failed
- Ensure MongoDB is running: `mongod`
- Check `MONGO_URI` in `.env` file
- Verify MongoDB is listening on the configured port

### Port Already in Use
Change the `PORT` in `.env` to an available port (e.g., 5001)

### Excel file import fails
- Ensure columns are named exactly as specified
- Check that email addresses are valid
- Verify the file is a valid Excel file (.xlsx or .xls)

### Duplicate Email Errors
The API detects and prevents duplicate users with the same email. To re-import with the same emails, clear the database first or manually remove duplicate entries.

---

## Next Steps

1. Start the server: `python server.py`
2. Access API docs: http://localhost:5000/docs
3. Run tests: `python test_apis.py`
4. Integrate with your frontend or other services

---

## Support

For issues or questions, check the test scripts and error messages for detailed information about failures.
