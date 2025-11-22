from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from app import database
from app.services.email_sender import send_email
from app.services.public_api import get_todos, format_todos_message, get_posts, format_posts_message
from app.config import settings
import pytz
from bson import ObjectId

scheduler = AsyncIOScheduler(timezone=settings.SCHEDULER_TIMEZONE)


async def send_scheduled_email(schedule_id: str):
    try:
        obj_id = ObjectId(schedule_id)
    except Exception as e:
        print(f"Invalid schedule ID format: {schedule_id} - {str(e)}")
        return
    
    schedule = await database.db.schedules.find_one({"_id": obj_id})
    
    if not schedule:
        print(f"Schedule {schedule_id} not found")
        return
    
    if schedule["status"] != "pending":
        print(f"Schedule {schedule_id} is not pending (current status: {schedule['status']})")
        return
    
    message_body = schedule["message"]
    
    user_id = schedule.get("user_id", 1)
    
    # Add todos if requested
    if schedule.get("include_todos"):
        todos = get_todos(user_id)
        todos_text = format_todos_message(todos)
        if todos_text:
            message_body += todos_text
    
    # Always add posts from JSONPlaceholder API
    posts = get_posts(user_id)
    posts_text = format_posts_message(posts)
    if posts_text:
        message_body += posts_text
    
    success = send_email(
        to_email=schedule["email"],
        subject="Scheduled Email",
        body=message_body
    )
    
    if success:
        await database.db.schedules.update_one(
            {"_id": obj_id},
            {"$set": {"status": "sent", "sent_at": datetime.utcnow()}}
        )
        print(f"Email sent successfully for schedule {schedule_id}")
    else:
        await database.db.schedules.update_one(
            {"_id": obj_id},
            {"$set": {"status": "failed"}}
        )
        print(f"Email failed to send for schedule {schedule_id}")


def schedule_email(schedule_id: str, scheduled_time: datetime, timezone_str: str):
    try:
        tz = pytz.timezone(timezone_str)
        scheduled_time_aware = tz.localize(scheduled_time.replace(tzinfo=None))
        
        scheduler.add_job(
            send_scheduled_email,
            trigger=DateTrigger(run_date=scheduled_time_aware),
            args=[schedule_id],
            id=schedule_id,
            replace_existing=True
        )
        
        print(f"Email scheduled for {scheduled_time_aware}")
    except Exception as e:
        print(f"Failed to schedule email: {e}")


def cancel_scheduled_email(schedule_id: str):
    try:
        scheduler.remove_job(schedule_id)
        print(f"Schedule cancelled: {schedule_id}")
    except Exception as e:
        print(f"Failed to cancel: {e}")


def start_scheduler():
    if not scheduler.running:
        scheduler.start()
        print("Scheduler started")


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("Scheduler stopped")

