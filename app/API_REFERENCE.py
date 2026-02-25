"""
COMPLETE LIST OF ALL APIs IN THE PROJECT
==========================================

This file provides a quick reference for all available APIs
"""

# =====================================================
# USER MANAGEMENT APIs (Base: /api/users)
# =====================================================

USERS_API = {
    "1. Create User": {
        "Method": "POST",
        "Endpoint": "/api/users/",
        "Body": {"name", "email", "role"},
        "Response": {"status", "message", "user_id"}
    },
    "2. Get All Users": {
        "Method": "GET",
        "Endpoint": "/api/users/",
        "Response": {"status", "message", "total", "data"}
    },
    "3. Get User by ID": {
        "Method": "GET",
        "Endpoint": "/api/users/{user_id}",
        "Response": {"status", "message", "data"}
    },
    "4. Update User": {
        "Method": "PUT",
        "Endpoint": "/api/users/{user_id}",
        "Body": {"name", "email", "role"},
        "Response": {"status", "message", "user_id"}
    },
    "5. Delete User": {
        "Method": "DELETE",
        "Endpoint": "/api/users/{user_id}",
        "Response": {"status", "message", "user_id"}
    }
}

# =====================================================
# SERVER MANAGEMENT APIs (Base: /api/servers)
# =====================================================

SERVERS_API = {
    "1. Create Server": {
        "Method": "POST",
        "Endpoint": "/api/servers/create",
        "Body": {"user_id", "name", "hostname", "port", "status", "connection_name", "instance_url", "username", "password"},
        "Response": {"status", "message", "server_id"}
    },
    "2. Get All Servers": {
        "Method": "GET",
        "Endpoint": "/api/servers/",
        "Response": {"status", "message", "total", "data"}
    },
    "3. Get Server by ID": {
        "Method": "GET",
        "Endpoint": "/api/servers/{server_id}",
        "Response": {"status", "message", "data"}
    },
    "4. Get Servers by User": {
        "Method": "GET",
        "Endpoint": "/api/servers/user/{user_id}",
        "Response": {"status", "message", "total", "data"}
    }
}

# =====================================================
# SCHEDULER JOB APIs (Base: /api/scheduler/jobs)
# =====================================================

SCHEDULER_JOBS_API = {
    "1. Create Scheduled Job": {
        "Method": "POST",
        "Endpoint": "/api/scheduler/jobs",
        "Body": {
            "user_id": "Required",
            "job_class_string": "Required",
            "name": "Required",
            "description": "Optional",
            "minute": "Optional (default: *)",
            "hour": "Optional (default: *)",
            "day_of_month": "Optional (default: *)",
            "month": "Optional (default: *)",
            "day_of_week": "Optional (default: *)",
            "week": "Optional (default: *)",
            "pub_args": "Optional list",
            "pub_kwargs": "Optional dict"
        },
        "Response": {"status", "message", "job_id"}
    },
    "2. Get All Jobs": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/jobs",
        "Response": {"status", "message", "total", "data"}
    },
    "3. Get Job by ID": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/jobs/{job_id}",
        "Response": {"status", "message", "data"}
    },
    "4. Get Jobs by User": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/users/{user_id}/jobs",
        "Response": {"status", "message", "total", "data"}
    },
    "5. Update Job": {
        "Method": "PUT",
        "Endpoint": "/api/scheduler/jobs/{job_id}",
        "Body": "Any field can be updated",
        "Response": {"status", "message", "job_id"}
    },
    "6. Delete Job": {
        "Method": "DELETE",
        "Endpoint": "/api/scheduler/jobs/{job_id}",
        "Response": {"status", "message", "job_id"}
    },
    "7. Pause Job": {
        "Method": "PATCH",
        "Endpoint": "/api/scheduler/jobs/{job_id}/pause",
        "Response": {"status", "message", "job_id"}
    },
    "8. Resume Job": {
        "Method": "PATCH",
        "Endpoint": "/api/scheduler/jobs/{job_id}/resume",
        "Response": {"status", "message", "job_id"}
    },
    "9. Run Job Immediately": {
        "Method": "POST",
        "Endpoint": "/api/scheduler/jobs/{job_id}/run",
        "Response": {"status", "message", "execution_id"}
    }
}

# =====================================================
# SCHEDULER EXECUTION APIs (Base: /api/scheduler/executions)
# =====================================================

SCHEDULER_EXECUTIONS_API = {
    "1. Get Executions": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/executions",
        "QueryParams": {"job_id": "Optional"},
        "Response": {"status", "message", "total", "data"}
    },
    "2. Get Execution by ID": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/executions/{execution_id}",
        "Response": {"status", "message", "data"}
    }
}

# =====================================================
# SCHEDULER UTILITY APIs (Base: /api/scheduler)
# =====================================================

SCHEDULER_UTILITY_API = {
    "1. Get Available Jobs": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/available-jobs",
        "Response": {"status", "message", "total", "jobs"}
    },
    "2. Get Scheduler Stats": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/stats",
        "QueryParams": {"user_id": "Optional"},
        "Response": {
            "status": "str",
            "message": "str",
            "stats": {
                "total_jobs": "int",
                "enabled_jobs": "int",
                "paused_jobs": "int",
                "total_executions": "int",
                "completed_executions": "int",
                "failed_executions": "int",
                "success_rate": "float"
            }
        }
    },
    "3. Health Check": {
        "Method": "GET",
        "Endpoint": "/api/scheduler/health",
        "Response": {"status", "message", "timestamp"}
    }
}

# =====================================================
# AVAILABLE JOB CLASSES
# =====================================================

AVAILABLE_JOBS = {
    "jobs.echo.EchoJob": "Simple job that echoes arguments",
    "jobs.server.ServerHealthCheckJob": "Check server health status",
    "jobs.backup.DataBackupJob": "Backup database",
    "jobs.email.EmailNotificationJob": "Send email notifications",
    "jobs.cleanup.DataCleanupJob": "Clean up old data",
    "jobs.metrics.SystemMetricsJob": "Collect system metrics",
    "jobs.report.ReportGenerationJob": "Generate reports",
    "jobs.webhook.WebhookJob": "Send webhook notifications",
    "jobs.maintenance.MaintenanceJob": "Run maintenance tasks",
    "jobs.custom.CustomScriptJob": "Run custom scripts"
}

# =====================================================
# QUICK STATISTICS
# =====================================================

STATISTICS = {
    "Total User APIs": 5,
    "Total Server APIs": 4,
    "Total Scheduler Job APIs": 9,
    "Total Execution APIs": 2,
    "Total Utility APIs": 3,
    "Available Job Classes": 10,
    "Total Endpoints": 23
}

# =====================================================
# STATUS CODES
# =====================================================

STATUS_CODES = {
    "200": "OK - Request succeeded",
    "201": "Created - Resource created",
    "400": "Bad Request - Invalid input",
    "404": "Not Found - Resource not found",
    "500": "Internal Server Error - Server error",
    "503": "Service Unavailable - Service down"
}

if __name__ == "__main__":
    print("\n" + "="*70)
    print("COMPLETE API REFERENCE - TEXIUM BACKEND WITH SCHEDULER")
    print("="*70)
    
    print("\n📋 USER MANAGEMENT APIs (5 endpoints)")
    for api_name, details in USERS_API.items():
        print(f"  {api_name}: {details['Method']} {details['Endpoint']}")
    
    print("\n📋 SERVER MANAGEMENT APIs (4 endpoints)")
    for api_name, details in SERVERS_API.items():
        print(f"  {api_name}: {details['Method']} {details['Endpoint']}")
    
    print("\n📋 SCHEDULER JOB APIs (9 endpoints)")
    for api_name, details in SCHEDULER_JOBS_API.items():
        print(f"  {api_name}: {details['Method']} {details['Endpoint']}")
    
    print("\n📋 SCHEDULER EXECUTION APIs (2 endpoints)")
    for api_name, details in SCHEDULER_EXECUTIONS_API.items():
        print(f"  {api_name}: {details['Method']} {details['Endpoint']}")
    
    print("\n📋 SCHEDULER UTILITY APIs (3 endpoints)")
    for api_name, details in SCHEDULER_UTILITY_API.items():
        print(f"  {api_name}: {details['Method']} {details['Endpoint']}")
    
    print("\n🔧 AVAILABLE JOB CLASSES (10 jobs)")
    for i, (job_class, description) in enumerate(AVAILABLE_JOBS.items(), 1):
        print(f"  {i}. {job_class}")
        print(f"     └─ {description}")
    
    print("\n📊 STATISTICS")
    for stat, value in STATISTICS.items():
        print(f"  • {stat}: {value}")
    
    print("\n✓ All APIs are documented and ready to use!")
    print("="*70 + "\n")
