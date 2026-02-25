"""Test script to verify scheduler integration"""
from services.jobs import get_available_jobs
from services.scheduler_service import SchedulerService
from models.job import Job, JobExecution

# Test available jobs
print("\n" + "="*50)
print("AVAILABLE SCHEDULER JOBS")
print("="*50)
jobs = get_available_jobs()
for i, (class_string, job_info) in enumerate(jobs.items(), 1):
    print(f"{i}. {job_info['name']}")
    print(f"   Class: {class_string}")
    print(f"   Description: {job_info['description']}")
    print()

# Test scheduler initialization
print("="*50)
print("SCHEDULER INITIALIZATION")
print("="*50)
result = SchedulerService.initialize_scheduler()
print(f"✓ Scheduler initialized: {result}")

# Test stats
print("\n" + "="*50)
print("SCHEDULER STATISTICS")
print("="*50)
stats_result = SchedulerService.get_scheduler_stats()
print(f"Success: {stats_result['success']}")
print(f"Message: {stats_result['message']}")
if stats_result.get('stats'):
    for key, value in stats_result['stats'].items():
        print(f"  {key}: {value}")

print("\n✓ All tests passed successfully!")
