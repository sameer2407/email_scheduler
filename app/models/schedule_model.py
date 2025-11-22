from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class ScheduleCreate(BaseModel):
    email: EmailStr
    message: str
    scheduled_time: datetime
    timezone: str = "UTC"
    include_todos: bool = False
    user_id: Optional[int] = 1


class ScheduleResponse(BaseModel):
    id: str
    email: str
    message: str
    scheduled_time: datetime
    timezone: str
    status: str
    include_todos: bool
    user_id: Optional[int]
    created_at: datetime
    sent_at: Optional[datetime] = None


class ScheduleUpdate(BaseModel):
    email: Optional[EmailStr] = None
    message: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    timezone: Optional[str] = None
    status: Optional[str] = None
    include_todos: Optional[bool] = None
    user_id: Optional[int] = None

