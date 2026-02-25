# 📋 COMPLETE API ENDPOINTS REFERENCE

## All APIs Available in Your Texium Backend Application

---

## 🟦 USER MANAGEMENT APIS (5 Endpoints)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 1 | POST | `/api/users/` | Create a new user |
| 2 | GET | `/api/users/` | Get all users |
| 3 | GET | `/api/users/{user_id}` | Get specific user |
| 4 | PUT | `/api/users/{user_id}` | Update user |
| 5 | DELETE | `/api/users/{user_id}` | Delete user |

---

## 🟩 SERVER MANAGEMENT APIS (4 Endpoints)

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 6 | POST | `/api/servers/create` | Create a new server |
| 7 | GET | `/api/servers/` | Get all servers |
| 8 | GET | `/api/servers/{server_id}` | Get specific server |
| 9 | GET | `/api/servers/user/{user_id}` | Get servers by user |

---

## 🟦 SCHEDULER JOB MANAGEMENT APIS (9 Endpoints) ⭐ NEW

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 10 | POST | `/api/scheduler/jobs` | Create new scheduled job |
| 11 | GET | `/api/scheduler/jobs` | Get all jobs |
| 12 | GET | `/api/scheduler/jobs/{job_id}` | Get specific job |
| 13 | GET | `/api/scheduler/users/{user_id}/jobs` | Get user's jobs |
| 14 | PUT | `/api/scheduler/jobs/{job_id}` | Update job |
| 15 | DELETE | `/api/scheduler/jobs/{job_id}` | Delete job |
| 16 | PATCH | `/api/scheduler/jobs/{job_id}/pause` | Pause job |
| 17 | PATCH | `/api/scheduler/jobs/{job_id}/resume` | Resume job |
| 18 | POST | `/api/scheduler/jobs/{job_id}/run` | Run job immediately |

---

## 🟪 JOB EXECUTION APIS (2 Endpoints) ⭐ NEW

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 19 | GET | `/api/scheduler/executions` | Get all executions |
| 20 | GET | `/api/scheduler/executions/{execution_id}` | Get specific execution |

---

## 🟨 SCHEDULER UTILITY APIS (3 Endpoints) ⭐ NEW

| # | Method | Endpoint | Description |
|---|--------|----------|-------------|
| 21 | GET | `/api/scheduler/available-jobs` | List available job classes |
| 22 | GET | `/api/scheduler/stats` | Get scheduler statistics |
| 23 | GET | `/api/scheduler/health` | Health check |

---

## 📊 STATISTICS

```
📈 Total Endpoints in Application: 23
   • User Management:     5 endpoints
   • Server Management:   4 endpoints
   • Scheduler Jobs:      9 endpoints ⭐
   • Executions:          2 endpoints ⭐
   • Utilities:           3 endpoints ⭐

🆕 New Scheduler Endpoints:     14 endpoints
📦 Available Job Classes:        10 pre-built jobs
💾 Database Collections:         2 new collections
🔍 Database Indexes:             6 new indexes
```

---

## 🎯 QUICK API EXAMPLES

### Create a Scheduled Job
```bash
curl -X POST http://localhost:8000/api/scheduler/jobs \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "507f1f77bcf86cd799439011",
    "job_class_string": "jobs.echo.EchoJob",
    "name": "Daily Task",
    "minute": "0",
    "hour": "9",
    "pub_args": ["Hello", "World"]
  }'
```

### Run Job Immediately
```bash
curl -X POST http://localhost:8000/api/scheduler/jobs/{job_id}/run
```

### Get All Jobs
```bash
curl http://localhost:8000/api/scheduler/jobs
```

### Get Executions
```bash
curl http://localhost:8000/api/scheduler/executions
```

### Get Statistics
```bash
curl http://localhost:8000/api/scheduler/stats
```

### Health Check
```bash
curl http://localhost:8000/api/scheduler/health
```

---

## 🧩 AVAILABLE JOB CLASSES (10 Jobs)

```
1. jobs.echo.EchoJob
   → Echo arguments for testing

2. jobs.server.ServerHealthCheckJob
   → Monitor server health status

3. jobs.backup.DataBackupJob
   → Backup database

4. jobs.email.EmailNotificationJob
   → Send email notifications

5. jobs.cleanup.DataCleanupJob
   → Clean up old data

6. jobs.metrics.SystemMetricsJob
   → Collect system metrics

7. jobs.report.ReportGenerationJob
   → Generate reports

8. jobs.webhook.WebhookJob
   → Send webhook notifications

9. jobs.maintenance.MaintenanceJob
   → Run maintenance tasks

10. jobs.custom.CustomScriptJob
    → Execute custom scripts
```

---

## 📍 SERVER CONFIGURATION

```
Base URL:      http://localhost:8000
API Prefix:    /api
API Docs:      /docs (Swagger UI)
ReDoc:         /redoc

Environment:
- Python:      3.9+
- Framework:   FastAPI
- Server:      Uvicorn
- Database:    MongoDB
```

---

## 🚀 STARTUP COMMAND

```bash
cd d:\reactcheck\TexiumBackend
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

Then visit: **http://localhost:8000/docs**

---

## 💡 COMMON USE CASES

### Daily Report Generation
```
Endpoint:     POST /api/scheduler/jobs
Job Class:    jobs.report.ReportGenerationJob
Schedule:     Every day at 9 AM
pub_kwargs:   {"report_type": "daily"}
```

### Server Health Monitoring
```
Endpoint:     POST /api/scheduler/jobs
Job Class:    jobs.server.ServerHealthCheckJob
Schedule:     Every hour
pub_args:     [server_id]
```

### Weekly Database Backup
```
Endpoint:     POST /api/scheduler/jobs
Job Class:    jobs.backup.DataBackupJob
Schedule:     Every Sunday at midnight
pub_kwargs:   {"collections": ["users", "servers"]}
```

### Team Notifications
```
Endpoint:     POST /api/scheduler/jobs
Job Class:    jobs.email.EmailNotificationJob
Schedule:     Every Monday at 9 AM
pub_args:     [team_email@example.com]
pub_kwargs:   {"subject": "Standup", "message": "..."}
```

---

## 🔐 RESPONSE FORMAT

All endpoints return consistent JSON:

### Success Response
```json
{
  "status": "success",
  "message": "Operation successful",
  "data": {...}
}
```

### Error Response
```json
{
  "detail": "Error message"
}
```

---

## 📚 DOCUMENTATION REFERENCE

| Document | Purpose |
|----------|---------|
| **API_DOCUMENTATION.md** | Complete API guide with examples |
| **API_REFERENCE.py** | Python API reference |
| **TEST_SCHEDULER_APIS.sh** | cURL testing examples |
| **SCHEDULER_INTEGRATION_SUMMARY.md** | Integration details |
| **PROJECT_COMPLETE_SUMMARY.md** | Project overview |
| **This file** | Quick endpoint reference |

---

## ✅ VERIFICATION

To verify all APIs are working:

```bash
python test_scheduler.py
```

Expected output:
```
✓ 10 job classes available
✓ Scheduler initialized
✓ Statistics retrieved
✓ All tests passed
```

---

## 🎯 NEXT STEPS

1. ✅ Start the server: `uvicorn server:app --reload`
2. ✅ Check API docs: Visit http://localhost:8000/docs
3. ✅ Create first job: Use POST `/api/scheduler/jobs`
4. ✅ Run immediately: Use POST `/api/scheduler/jobs/{job_id}/run`
5. ✅ Check results: Use GET `/api/scheduler/executions`

---

## 📞 SUPPORT

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **API Reference:** See `API_DOCUMENTATION.md`
- **Examples:** See `TEST_SCHEDULER_APIS.sh`

---

**Ready to use! 🚀**

All 23 APIs are documented and production-ready.

Start scheduling jobs with your FastAPI backend!

Version: 2.0.0 | Date: Feb 23, 2026
