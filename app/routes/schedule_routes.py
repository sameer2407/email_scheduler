from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.schedule_model import ScheduleCreate, ScheduleResponse, ScheduleUpdate
from app import database
from app.services.scheduler import schedule_email, cancel_scheduled_email
from bson import ObjectId

router = APIRouter(prefix="/schedules", tags=["Schedules"])


def schedule_to_response(schedule: dict) -> dict:
    schedule["id"] = str(schedule["_id"])
    del schedule["_id"]
    return schedule


@router.post("/", response_model=ScheduleResponse)
async def create_schedule(schedule: ScheduleCreate):
    schedule_dict = schedule.model_dump()
    schedule_dict["status"] = "pending"
    schedule_dict["created_at"] = datetime.utcnow()
    schedule_dict["sent_at"] = None
    
    result = await database.db.schedules.insert_one(schedule_dict)
    schedule_id = str(result.inserted_id)
    
    schedule_email(
        schedule_id=schedule_id,
        scheduled_time=schedule.scheduled_time,
        timezone_str=schedule.timezone
    )
    
    schedule_dict["_id"] = result.inserted_id
    return schedule_to_response(schedule_dict)


@router.get("/", response_model=List[ScheduleResponse])
async def get_schedules(status: str = None):
    query = {}
    if status:
        query["status"] = status
    
    schedules = await database.db.schedules.find(query).to_list(length=100)
    return [schedule_to_response(s) for s in schedules]


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(schedule_id: str):
    try:
        schedule = await database.db.schedules.find_one({"_id": ObjectId(schedule_id)})
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    if not schedule:
        raise HTTPException(status_code=404, detail="Not found")
    
    return schedule_to_response(schedule)


@router.put("/{schedule_id}", response_model=ScheduleResponse)
async def update_schedule(schedule_id: str, schedule_update: ScheduleUpdate):
    try:
        obj_id = ObjectId(schedule_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    existing = await database.db.schedules.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(status_code=404, detail="Not found")
    
    update_data = {k: v for k, v in schedule_update.model_dump().items() if v is not None}
    
    if update_data:
        await database.db.schedules.update_one({"_id": obj_id}, {"$set": update_data})
        
        if "scheduled_time" in update_data or "timezone" in update_data:
            cancel_scheduled_email(schedule_id)
            schedule_email(
                schedule_id=schedule_id,
                scheduled_time=update_data.get("scheduled_time", existing["scheduled_time"]),
                timezone_str=update_data.get("timezone", existing["timezone"])
            )
    
    updated_schedule = await database.db.schedules.find_one({"_id": obj_id})
    return schedule_to_response(updated_schedule)


@router.delete("/{schedule_id}")
async def delete_schedule(schedule_id: str):
    try:
        obj_id = ObjectId(schedule_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID")
    
    result = await database.db.schedules.delete_one({"_id": obj_id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    
    cancel_scheduled_email(schedule_id)
    
    return {"message": "Deleted successfully"}

