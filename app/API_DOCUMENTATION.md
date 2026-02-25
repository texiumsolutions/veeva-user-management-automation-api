# Complete API Documentation - Texium Backend with Scheduler Integration

## Overview
This is the complete API documentation for the Texium Backend application, which includes user management, server management, and job scheduling functionality integrated with ndscheduler.

---

## Table of Contents
1. [User Management APIs](#user-management-apis)
2. [Server Management APIs](#server-management-apis)
3. [Scheduler Job APIs](#scheduler-job-apis)
4. [Scheduler Execution APIs](#scheduler-execution-apis)
5. [Scheduler Utility APIs](#scheduler-utility-apis)

---

## User Management APIs

### 1. Create User
**Endpoint:** `POST /api/users/`
**Description:** Create a new user
**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "role": "admin"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "User created successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

### 2. Get All Users
**Endpoint:** `GET /api/users/`
**Description:** Retrieve all users
**Response:**
```json
{
  "status": "success",
  "message": "Users retrieved successfully",
  "total": 5,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "name": "John Doe",
      "email": "john@example.com",
      "role": "admin",
      "created_at": "2026-02-23T10:00:00",
      "updated_at": "2026-02-23T10:00:00"
    }
  ]
}
```

### 3. Get User by ID
**Endpoint:** `GET /api/users/{user_id}`
**Description:** Get a specific user
**Response:**
```json
{
  "status": "success",
  "message": "User retrieved successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "role": "admin",
    "created_at": "2026-02-23T10:00:00",
    "updated_at": "2026-02-23T10:00:00"
  }
}
```

### 4. Update User
**Endpoint:** `PUT /api/users/{user_id}`
**Description:** Update user information
**Request Body:**
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "user"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "User updated successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

### 5. Delete User
**Endpoint:** `DELETE /api/users/{user_id}`
**Description:** Delete a user
**Response:**
```json
{
  "status": "success",
  "message": "User deleted successfully",
  "user_id": "507f1f77bcf86cd799439011"
}
```

---

## Server Management APIs

### 1. Create Server
**Endpoint:** `POST /api/servers/create`
**Description:** Create a new server
**Request Body:**
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "name": "Production Server",
  "hostname": "prod.example.com",
  "port": 8080,
  "status": "running",
  "connection_name": "ServiceNow Connection",
  "instance_url": "https://dev123456.service-now.com",
  "username": "admin",
  "password": "password123"
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Server Production Server created successfully",
  "server_id": "507f1f77bcf86cd799439012"
}
```

### 2. Get All Servers
**Endpoint:** `GET /api/servers/`
**Description:** Retrieve all servers
**Response:**
```json
{
  "status": "success",
  "message": "Servers retrieved successfully",
  "total": 3,
  "data": [...]
}
```

### 3. Get Server by ID
**Endpoint:** `GET /api/servers/{server_id}`
**Description:** Get a specific server
**Response:**
```json
{
  "status": "success",
  "message": "Server retrieved successfully",
  "data": {
    "_id": "507f1f77bcf86cd799439012",
    "user_id": "507f1f77bcf86cd799439011",
    "name": "Production Server",
    "hostname": "prod.example.com",
    "port": 8080,
    "status": "running",
    "connection_name": "ServiceNow Connection",
    "instance_url": "https://dev123456.service-now.com",
    "created_at": "2026-02-23T10:00:00",
    "updated_at": "2026-02-23T10:00:00"
  }
}
```

### 4. Get Servers by User
**Endpoint:** `GET /api/servers/user/{user_id}`
**Description:** Get all servers for a specific user
**Response:**
```json
{
  "status": "success",
  "message": "Servers retrieved successfully",
  "total": 2,
  "data": [...]
}
```

---

## Scheduler Job APIs

### 1. Create a Scheduled Job
**Endpoint:** `POST /api/scheduler/jobs`
**Description:** Create a new scheduled job
**Request Body:**
```json
{
  "user_id": "507f1f77bcf86cd799439011",
  "job_class_string": "jobs.echo.EchoJob",
  "name": "Daily Echo Job",
  "description": "Runs echo job daily",
  "minute": "0",
  "hour": "9",
  "day_of_month": "*",
  "month": "*",
  "day_of_week": "*",
  "pub_args": ["arg1", "arg2"],
  "pub_kwargs": {"key": "value"}
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Job 'Daily Echo Job' created successfully",
  "job_id": "507f1f77bcf86cd799439013"
}
```

### 2. Get All Jobs
**Endpoint:** `GET /api/scheduler/jobs`
**Description:** Retrieve all scheduled jobs
**Response:**
```json
{
  "status": "success",
  "message": "Jobs retrieved successfully",
  "total": 5,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439013",
      "user_id": "507f1f77bcf86cd799439011",
      "job_class_string": "jobs.echo.EchoJob",
      "name": "Daily Echo Job",
      "description": "Runs echo job daily",
      "minute": "0",
      "hour": "9",
      "day_of_month": "*",
      "month": "*",
      "day_of_week": "*",
      "week": "*",
      "pub_args": ["arg1", "arg2"],
      "pub_kwargs": {"key": "value"},
      "is_enabled": true,
      "is_paused": false,
      "created_at": "2026-02-23T10:00:00",
      "updated_at": "2026-02-23T10:00:00",
      "last_run_time": null,
      "next_run_time": null,
      "total_executions": 0
    }
  ]
}
```

### 3. Get Job by ID
**Endpoint:** `GET /api/scheduler/jobs/{job_id}`
**Description:** Get a specific job
**Response:** Returns single job object (same structure as above)

### 4. Get Jobs by User
**Endpoint:** `GET /api/scheduler/users/{user_id}/jobs`
**Description:** Get all jobs for a specific user
**Response:**
```json
{
  "status": "success",
  "message": "Jobs retrieved successfully",
  "total": 3,
  "data": [...]
}
```

### 5. Update a Job
**Endpoint:** `PUT /api/scheduler/jobs/{job_id}`
**Description:** Update a scheduled job
**Request Body:**
```json
{
  "name": "Updated Echo Job",
  "description": "Updated description",
  "minute": "*/5",
  "hour": "*",
  "is_enabled": true
}
```
**Response:**
```json
{
  "status": "success",
  "message": "Job updated successfully",
  "job_id": "507f1f77bcf86cd799439013"
}
```

### 6. Delete a Job
**Endpoint:** `DELETE /api/scheduler/jobs/{job_id}`
**Description:** Delete a scheduled job
**Response:**
```json
{
  "status": "success",
  "message": "Job deleted successfully",
  "job_id": "507f1f77bcf86cd799439013"
}
```

### 7. Pause a Job
**Endpoint:** `PATCH /api/scheduler/jobs/{job_id}/pause`
**Description:** Pause a scheduled job
**Response:**
```json
{
  "status": "success",
  "message": "Job paused successfully",
  "job_id": "507f1f77bcf86cd799439013"
}
```

### 8. Resume a Job
**Endpoint:** `PATCH /api/scheduler/jobs/{job_id}/resume`
**Description:** Resume a paused job
**Response:**
```json
{
  "status": "success",
  "message": "Job resumed successfully",
  "job_id": "507f1f77bcf86cd799439013"
}
```

### 9. Run a Job Immediately
**Endpoint:** `POST /api/scheduler/jobs/{job_id}/run`
**Description:** Execute a job immediately (create an execution)
**Response:**
```json
{
  "status": "success",
  "message": "Job execution started",
  "execution_id": "507f1f77bcf86cd799439014"
}
```

---

## Scheduler Execution APIs

### 1. Get Executions
**Endpoint:** `GET /api/scheduler/executions`
**Description:** Get job executions (optionally filtered by job_id)
**Query Parameters:**
- `job_id` (optional): Filter by specific job
**Response:**
```json
{
  "status": "success",
  "message": "Executions retrieved successfully",
  "total": 10,
  "data": [
    {
      "_id": "507f1f77bcf86cd799439014",
      "job_id": "507f1f77bcf86cd799439013",
      "user_id": "507f1f77bcf86cd799439011",
      "job_name": "Daily Echo Job",
      "job_class_string": "jobs.echo.EchoJob",
      "status": "completed",
      "output": "Echo Job executed at 2026-02-23T10:00:00\nArgs: ['arg1', 'arg2']\nKwargs: {'key': 'value'}\n",
      "error": "",
      "started_at": "2026-02-23T09:00:00",
      "completed_at": "2026-02-23T09:00:05",
      "created_at": "2026-02-23T09:00:00"
    }
  ]
}
```

### 2. Get Execution by ID
**Endpoint:** `GET /api/scheduler/executions/{execution_id}`
**Description:** Get a specific execution
**Response:** Returns single execution object (same structure as above)

---

## Scheduler Utility APIs

### 1. Get Available Jobs
**Endpoint:** `GET /api/scheduler/available-jobs`
**Description:** Get list of all available job classes that can be scheduled
**Response:**
```json
{
  "status": "success",
  "message": "Available jobs retrieved successfully",
  "total": 10,
  "jobs": [
    {
      "class_string": "jobs.echo.EchoJob",
      "name": "EchoJob",
      "description": "Simple job that echoes arguments"
    },
    {
      "class_string": "jobs.server.ServerHealthCheckJob",
      "name": "ServerHealthCheckJob",
      "description": "Job to check server health status"
    },
    {
      "class_string": "jobs.backup.DataBackupJob",
      "name": "DataBackupJob",
      "description": "Job to backup database"
    },
    {
      "class_string": "jobs.email.EmailNotificationJob",
      "name": "EmailNotificationJob",
      "description": "Job to send email notifications"
    },
    {
      "class_string": "jobs.cleanup.DataCleanupJob",
      "name": "DataCleanupJob",
      "description": "Job to clean up old data"
    },
    {
      "class_string": "jobs.metrics.SystemMetricsJob",
      "name": "SystemMetricsJob",
      "description": "Job to collect system metrics"
    },
    {
      "class_string": "jobs.report.ReportGenerationJob",
      "name": "ReportGenerationJob",
      "description": "Job to generate reports"
    },
    {
      "class_string": "jobs.webhook.WebhookJob",
      "name": "WebhookJob",
      "description": "Job to send webhook notifications"
    },
    {
      "class_string": "jobs.maintenance.MaintenanceJob",
      "name": "MaintenanceJob",
      "description": "Job for maintenance tasks"
    },
    {
      "class_string": "jobs.custom.CustomScriptJob",
      "name": "CustomScriptJob",
      "description": "Job to run custom scripts"
    }
  ]
}
```

### 2. Get Scheduler Statistics
**Endpoint:** `GET /api/scheduler/stats`
**Description:** Get scheduler statistics (optionally for a specific user)
**Query Parameters:**
- `user_id` (optional): Filter stats by user
**Response:**
```json
{
  "status": "success",
  "message": "Stats retrieved successfully",
  "stats": {
    "total_jobs": 5,
    "enabled_jobs": 4,
    "paused_jobs": 1,
    "total_executions": 42,
    "completed_executions": 40,
    "failed_executions": 2,
    "success_rate": 95.23
  }
}
```

### 3. Scheduler Health Check
**Endpoint:** `GET /api/scheduler/health`
**Description:** Check if scheduler is healthy and running
**Response:**
```json
{
  "status": "healthy",
  "message": "Scheduler is running",
  "timestamp": null
}
```

---

## Available Job Classes

The scheduler comes with 10 predefined job classes that can be used:

### 1. **EchoJob** (`jobs.echo.EchoJob`)
- **Description:** Simple job that echoes arguments
- **Use Case:** Testing and debugging
- **Parameters:** 
  - `pub_args`: List of arguments to echo
  - `pub_kwargs`: Dictionary of keyword arguments

### 2. **ServerHealthCheckJob** (`jobs.server.ServerHealthCheckJob`)
- **Description:** Check server health status
- **Use Case:** Monitor server health
- **Parameters:**
  - `pub_args`: [server_id]

### 3. **DataBackupJob** (`jobs.backup.DataBackupJob`)
- **Description:** Backup database
- **Use Case:** Scheduled database backups
- **Parameters:**
  - `pub_kwargs`: {'collections': ['users', 'servers', 'jobs']}

### 4. **EmailNotificationJob** (`jobs.email.EmailNotificationJob`)
- **Description:** Send email notifications
- **Use Case:** Send scheduled emails
- **Parameters:**
  - `pub_args`: [recipient_email]
  - `pub_kwargs`: {'subject': '...', 'message': '...'}

### 5. **DataCleanupJob** (`jobs.cleanup.DataCleanupJob`)
- **Description:** Clean up old data
- **Use Case:** Database maintenance
- **Parameters:**
  - `pub_kwargs`: {'days_old': 30, 'collections': [...]}

### 6. **SystemMetricsJob** (`jobs.metrics.SystemMetricsJob`)
- **Description:** Collect system metrics
- **Use Case:** Monitor system performance
- **Parameters:** None

### 7. **ReportGenerationJob** (`jobs.report.ReportGenerationJob`)
- **Description:** Generate reports
- **Use Case:** Scheduled reporting
- **Parameters:**
  - `pub_kwargs`: {'report_type': 'daily|weekly|monthly'}

### 8. **WebhookJob** (`jobs.webhook.WebhookJob`)
- **Description:** Send webhook notifications
- **Use Case:** Notify external systems
- **Parameters:**
  - `pub_args`: [webhook_url]
  - `pub_kwargs`: {custom_data}

### 9. **MaintenanceJob** (`jobs.maintenance.MaintenanceJob`)
- **Description:** Run maintenance tasks
- **Use Case:** System maintenance
- **Parameters:**
  - `pub_kwargs`: {'tasks': ['rebuild_indexes', 'optimize_queries', 'clear_cache']}

### 10. **CustomScriptJob** (`jobs.custom.CustomScriptJob`)
- **Description:** Run custom scripts
- **Use Case:** Execute custom logic
- **Parameters:**
  - `pub_args`: [script_name]
  - `pub_kwargs`: {script_parameters}

---

## Cron Schedule Format

Jobs use Unix cron scheduling format. Here are examples:

- `minute`: "0" = minute 0
- `hour`: "9" = 9 AM
- `day_of_month`: "1" = 1st day of month
- `month`: "3" = March
- `day_of_week`: "1" = Monday (0=Sunday, 1=Monday, ..., 6=Saturday)
- `week`: "*" = every week

### Common Schedule Examples:
```
Every day at 9 AM:
  minute: "0", hour: "9", day_of_month: "*", month: "*", day_of_week: "*"

Every Monday at 3 PM:
  minute: "0", hour: "15", day_of_month: "*", month: "*", day_of_week: "1"

Every 5 minutes:
  minute: "*/5", hour: "*", day_of_month: "*", month: "*", day_of_week: "*"

First day of month at midnight:
  minute: "0", hour: "0", day_of_month: "1", month: "*", day_of_week: "*"
```

---

## Error Handling

All endpoints return structured error responses:

### 400 Bad Request
```json
{
  "detail": "Missing required field: name"
}
```

### 404 Not Found
```json
{
  "detail": "Job not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

---

## Running the Server

Start the application with:
```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Access API documentation at: `http://localhost:8000/docs`

---

## Database Collections

The application creates and uses the following MongoDB collections:

1. **users** - User information
2. **servers** - Server configurations
3. **scheduler_jobs** - Scheduled jobs
4. **scheduler_executions** - Job execution history

---

## Environment Variables

Create a `.env` file with:
```
MONGO_URI=mongodb://localhost:27017
DB_NAME=texium_db
```

---

## Integration with ndscheduler

This application integrates the following features from ndscheduler:

- Job scheduling with cron expressions
- Job execution management
- Execution history tracking
- Job state management (enabled/paused/disabled)
- Multiple built-in job types
- Extensible job architecture

The scheduler runs jobs in background threads and stores all execution results in MongoDB for auditing and monitoring.

---

**Version:** 2.0.0  
**Last Updated:** February 23, 2026
