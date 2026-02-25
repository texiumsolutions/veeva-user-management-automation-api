"""Sample scheduler jobs - Job classes that can be scheduled"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
import json
from datetime import datetime


class JobBase(ABC):
    """Base class for all scheduler jobs"""
    
    def __init__(self, pub_args: List = None, pub_kwargs: Dict = None):
        self.pub_args = pub_args or []
        self.pub_kwargs = pub_kwargs or {}
    
    @abstractmethod
    def run(self) -> str:
        """Run the job - must be implemented by subclasses"""
        pass


class EchoJob(JobBase):
    """Simple job that echoes arguments"""
    
    def run(self) -> str:
        """Echo job arguments"""
        output = f"Echo Job executed at {datetime.utcnow()}\n"
        output += f"Args: {self.pub_args}\n"
        output += f"Kwargs: {self.pub_kwargs}\n"
        return output


class ServerHealthCheckJob(JobBase):
    """Job to check server health status"""
    
    def run(self) -> str:
        """Check server health"""
        output = f"Server Health Check Job executed at {datetime.utcnow()}\n"
        
        if self.pub_args:
            server_id = self.pub_args[0] if len(self.pub_args) > 0 else None
            output += f"Checking server: {server_id}\n"
        
        # Simulate health check
        output += "Status: ✓ All servers are healthy\n"
        output += "- CPU Usage: 45%\n"
        output += "- Memory Usage: 62%\n"
        output += "- Disk Usage: 78%\n"
        
        return output


class DataBackupJob(JobBase):
    """Job to backup database"""
    
    def run(self) -> str:
        """Backup database"""
        output = f"Database Backup Job executed at {datetime.utcnow()}\n"
        
        backup_name = f"backup_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        output += f"Backup Name: {backup_name}\n"
        output += "Backup Status: In Progress...\n"
        output += f"Collections to backup: {self.pub_kwargs.get('collections', ['users', 'servers', 'jobs'])}\n"
        output += "Backup completed successfully!\n"
        output += f"Backup Size: 2.5 MB\n"
        
        return output


class EmailNotificationJob(JobBase):
    """Job to send email notifications"""
    
    def run(self) -> str:
        """Send email notification"""
        output = f"Email Notification Job executed at {datetime.utcnow()}\n"
        
        recipient = self.pub_args[0] if len(self.pub_args) > 0 else "admin@example.com"
        subject = self.pub_kwargs.get("subject", "Scheduled Notification")
        
        output += f"To: {recipient}\n"
        output += f"Subject: {subject}\n"
        output += f"Message: {self.pub_kwargs.get('message', 'Notification from scheduler')}\n"
        output += "Status: Email sent successfully!\n"
        
        return output


class DataCleanupJob(JobBase):
    """Job to clean up old data"""
    
    def run(self) -> str:
        """Clean up old data"""
        output = f"Data Cleanup Job executed at {datetime.utcnow()}\n"
        
        days_old = self.pub_kwargs.get("days_old", 30)
        collections = self.pub_kwargs.get("collections", ["scheduler_executions"])
        
        output += f"Cleaning up data older than {days_old} days\n"
        output += f"Collections: {collections}\n"
        output += "Deleted records:\n"
        output += "  - 1,234 old executions\n"
        output += "  - 56 orphaned audit logs\n"
        output += "Cleanup completed! Total freed space: 125 MB\n"
        
        return output


class SystemMetricsJob(JobBase):
    """Job to collect system metrics"""
    
    def run(self) -> str:
        """Collect system metrics"""
        output = f"System Metrics Job executed at {datetime.utcnow()}\n"
        
        metrics = {
            "cpu_usage": 42.5,
            "memory_usage": 58.3,
            "disk_usage": 71.2,
            "network_in": 1234567,
            "network_out": 987654,
            "active_connections": 123,
            "request_count": 5678
        }
        
        output += "System Metrics Collected:\n"
        for key, value in metrics.items():
            output += f"  {key}: {value}\n"
        
        return output


class ReportGenerationJob(JobBase):
    """Job to generate reports"""
    
    def run(self) -> str:
        """Generate report"""
        output = f"Report Generation Job executed at {datetime.utcnow()}\n"
        
        report_type = self.pub_kwargs.get("report_type", "daily")
        
        output += f"Generating {report_type} report...\n"
        output += "Report Details:\n"
        output += f"  - Total Jobs: 42\n"
        output += f"  - Executions Today: 156\n"
        output += f"  - Success Rate: 99.2%\n"
        output += f"  - Average Execution Time: 2.3s\n"
        output += f"Report saved: reports/{report_type}_{datetime.utcnow().strftime('%Y%m%d')}.pdf\n"
        
        return output


class WebhookJob(JobBase):
    """Job to send webhook notifications"""
    
    def run(self) -> str:
        """Send webhook notification"""
        output = f"Webhook Job executed at {datetime.utcnow()}\n"
        
        webhook_url = self.pub_args[0] if len(self.pub_args) > 0 else "https://example.com/webhook"
        
        payload = {
            "event": "scheduled_job",
            "timestamp": datetime.utcnow().isoformat(),
            "data": self.pub_kwargs
        }
        
        output += f"Sending webhook to: {webhook_url}\n"
        output += f"Payload: {json.dumps(payload, indent=2)}\n"
        output += "HTTP Status: 200 OK\n"
        output += "Webhook delivered successfully!\n"
        
        return output


class MaintenanceJob(JobBase):
    """Job for maintenance tasks"""
    
    def run(self) -> str:
        """Run maintenance tasks"""
        output = f"Maintenance Job executed at {datetime.utcnow()}\n"
        
        tasks = self.pub_kwargs.get("tasks", ["rebuild_indexes", "optimize_queries", "clear_cache"])
        
        output += "Running maintenance tasks...\n"
        for task in tasks:
            output += f"  ✓ {task}\n"
        
        output += "Database maintenance completed!\n"
        output += "Performance: +15% improvement\n"
        
        return output


class CustomScriptJob(JobBase):
    """Job to run custom scripts"""
    
    def run(self) -> str:
        """Run custom script"""
        output = f"Custom Script Job executed at {datetime.utcnow()}\n"
        
        script_name = self.pub_args[0] if len(self.pub_args) > 0 else "default_script.sh"
        
        output += f"Running script: {script_name}\n"
        output += f"Parameters: {self.pub_kwargs}\n"
        output += "Script Output:\n"
        output += "  Processing...\n"
        output += "  ✓ Step 1 completed\n"
        output += "  ✓ Step 2 completed\n"
        output += "  ✓ Step 3 completed\n"
        output += "Script executed successfully!\n"
        
        return output


# Registry of available jobs
AVAILABLE_JOBS = {
    "jobs.echo.EchoJob": EchoJob,
    "jobs.server.ServerHealthCheckJob": ServerHealthCheckJob,
    "jobs.backup.DataBackupJob": DataBackupJob,
    "jobs.email.EmailNotificationJob": EmailNotificationJob,
    "jobs.cleanup.DataCleanupJob": DataCleanupJob,
    "jobs.metrics.SystemMetricsJob": SystemMetricsJob,
    "jobs.report.ReportGenerationJob": ReportGenerationJob,
    "jobs.webhook.WebhookJob": WebhookJob,
    "jobs.maintenance.MaintenanceJob": MaintenanceJob,
    "jobs.custom.CustomScriptJob": CustomScriptJob,
}


def get_job_class(job_class_string: str) -> JobBase or None:
    """Get job class from registry"""
    return AVAILABLE_JOBS.get(job_class_string)


def get_available_jobs() -> Dict:
    """Get all available jobs"""
    jobs = {}
    for class_string, job_class in AVAILABLE_JOBS.items():
        jobs[class_string] = {
            "name": job_class.__name__,
            "description": job_class.__doc__,
            "class_string": class_string
        }
    return jobs
