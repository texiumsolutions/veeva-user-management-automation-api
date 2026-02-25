#!/bin/bash
# Example cURL Commands for Testing All Scheduler APIs
# Run these commands after starting the server: uvicorn server:app --reload

BASE_URL="http://localhost:8000"
USER_ID="507f1f77bcf86cd799439011"  # Replace with actual user ID

echo "======================================"
echo "SCHEDULER API Testing Examples"
echo "======================================"
echo ""

# =================== GET AVAILABLE JOBS ===================
echo "1️⃣  Get Available Jobs"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/available-jobs"
echo ""

# =================== CREATE A JOB ===================
echo "2️⃣  Create a New Job (Echo Job)"
echo "Command:"
curl_cmd="curl -X POST $BASE_URL/api/scheduler/jobs \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"user_id\": \"$USER_ID\",
    \"job_class_string\": \"jobs.echo.EchoJob\",
    \"name\": \"My Echo Job\",
    \"description\": \"A simple echo job for testing\",
    \"minute\": \"*/5\",
    \"hour\": \"*\",
    \"pub_args\": [\"Hello\", \"World\"],
    \"pub_kwargs\": {\"message\": \"Testing scheduler\"}
  }'"
echo "$curl_cmd"
echo ""

# =================== GET ALL JOBS ===================
echo "3️⃣  Get All Jobs"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/jobs"
echo ""

# =================== CREATE SERVER HEALTH CHECK JOB ===================
echo "4️⃣  Create Server Health Check Job"
echo "Command:"
curl_cmd="curl -X POST $BASE_URL/api/scheduler/jobs \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"user_id\": \"$USER_ID\",
    \"job_class_string\": \"jobs.server.ServerHealthCheckJob\",
    \"name\": \"Daily Server Health Check\",
    \"description\": \"Check server health every hour\",
    \"minute\": \"0\",
    \"hour\": \"*\",
    \"pub_args\": [\"server_123\"]
  }'"
echo "$curl_cmd"
echo ""

# =================== CREATE DATA BACKUP JOB ===================
echo "5️⃣  Create Data Backup Job"
echo "Command:"
curl_cmd="curl -X POST $BASE_URL/api/scheduler/jobs \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"user_id\": \"$USER_ID\",
    \"job_class_string\": \"jobs.backup.DataBackupJob\",
    \"name\": \"Daily Database Backup\",
    \"description\": \"Backup database daily at midnight\",
    \"minute\": \"0\",
    \"hour\": \"0\",
    \"day_of_month\": \"*\",
    \"month\": \"*\",
    \"day_of_week\": \"*\",
    \"pub_kwargs\": {
      \"collections\": [\"users\", \"servers\", \"scheduler_jobs\"]
    }
  }'"
echo "$curl_cmd"
echo ""

# =================== CREATE EMAIL NOTIFICATION JOB ===================
echo "6️⃣  Create Email Notification Job"
echo "Command:"
curl_cmd="curl -X POST $BASE_URL/api/scheduler/jobs \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"user_id\": \"$USER_ID\",
    \"job_class_string\": \"jobs.email.EmailNotificationJob\",
    \"name\": \"Weekly Team Standup\",
    \"description\": \"Send team standup reminder every Monday at 9 AM\",
    \"minute\": \"0\",
    \"hour\": \"9\",
    \"day_of_week\": \"1\",
    \"pub_args\": [\"team@example.com\"],
    \"pub_kwargs\": {
      \"subject\": \"Team Standup - Monday 9 AM\",
      \"message\": \"Hey team, time for our weekly standup!\"
    }
  }'"
echo "$curl_cmd"
echo ""

# =================== CREATE SYSTEM METRICS JOB ===================
echo "7️⃣  Create System Metrics Job"
echo "Command:"
curl_cmd="curl -X POST $BASE_URL/api/scheduler/jobs \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"user_id\": \"$USER_ID\",
    \"job_class_string\": \"jobs.metrics.SystemMetricsJob\",
    \"name\": \"Collect System Metrics\",
    \"description\": \"Collect system metrics every 5 minutes\",
    \"minute\": \"*/5\",
    \"hour\": \"*\"
  }'"
echo "$curl_cmd"
echo ""

# =================== GET JOBS FOR USER ===================
echo "8️⃣  Get Jobs for Specific User"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/users/$USER_ID/jobs"
echo ""

# =================== GET SPECIFIC JOB ===================
echo "9️⃣  Get Specific Job (Replace JOB_ID)"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/jobs/{JOB_ID}"
echo "Note: Replace {JOB_ID} with actual job ID from previous responses"
echo ""

# =================== UPDATE A JOB ===================
echo "🔟 Update a Job (Replace JOB_ID)"
echo "Command:"
curl_cmd="curl -X PUT $BASE_URL/api/scheduler/jobs/{JOB_ID} \\
  -H 'Content-Type: application/json' \\
  -d '{
    \"name\": \"Updated Job Name\",
    \"minute\": \"0\",
    \"hour\": \"12\",
    \"is_enabled\": true
  }'"
echo "$curl_cmd"
echo ""

# =================== RUN JOB IMMEDIATELY ===================
echo "1️⃣1️⃣  Run Job Immediately (Replace JOB_ID)"
echo "Command:"
echo "curl -X POST $BASE_URL/api/scheduler/jobs/{JOB_ID}/run"
echo ""

# =================== PAUSE A JOB ===================
echo "1️⃣2️⃣  Pause a Job (Replace JOB_ID)"
echo "Command:"
echo "curl -X PATCH $BASE_URL/api/scheduler/jobs/{JOB_ID}/pause"
echo ""

# =================== RESUME A JOB ===================
echo "1️⃣3️⃣  Resume a Job (Replace JOB_ID)"
echo "Command:"
echo "curl -X PATCH $BASE_URL/api/scheduler/jobs/{JOB_ID}/resume"
echo ""

# =================== GET EXECUTIONS ===================
echo "1️⃣4️⃣  Get All Executions"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/executions"
echo ""

# =================== GET EXECUTIONS FOR JOB ===================
echo "1️⃣5️⃣  Get Executions for Specific Job"
echo "Command:"
echo "curl -X GET '$BASE_URL/api/scheduler/executions?job_id={JOB_ID}'"
echo ""

# =================== GET SPECIFIC EXECUTION ===================
echo "1️⃣6️⃣  Get Specific Execution (Replace EXECUTION_ID)"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/executions/{EXECUTION_ID}"
echo ""

# =================== GET SCHEDULER STATS ===================
echo "1️⃣7️⃣  Get Scheduler Statistics"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/stats"
echo ""

# =================== GET STATS FOR USER ===================
echo "1️⃣8️⃣  Get Scheduler Stats for Specific User"
echo "Command:"
echo "curl -X GET '$BASE_URL/api/scheduler/stats?user_id=$USER_ID'"
echo ""

# =================== HEALTH CHECK ===================
echo "1️⃣9️⃣  Scheduler Health Check"
echo "Command:"
echo "curl -X GET $BASE_URL/api/scheduler/health"
echo ""

# =================== DELETE A JOB ===================
echo "2️⃣0️⃣  Delete a Job (Replace JOB_ID)"
echo "Command:"
echo "curl -X DELETE $BASE_URL/api/scheduler/jobs/{JOB_ID}"
echo ""

echo "======================================"
echo "✅ All test commands listed above!"
echo "======================================"
echo ""
echo "📝 Notes:"
echo "- Replace {JOB_ID} and {EXECUTION_ID} with actual IDs"
echo "- Replace $USER_ID with your actual user ID"
echo "- All responses are in JSON format"
echo "- Check the API_DOCUMENTATION.md for detailed endpoint info"
echo ""
