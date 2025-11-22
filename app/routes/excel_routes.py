import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from datetime import datetime
from app.utils.excel_reader import read_excel
from app import database
from app.services.scheduler import schedule_email

router = APIRouter(prefix="/excel", tags=["Excel"])


@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in ["xlsx", "xls"]:
        raise HTTPException(status_code=400, detail="Invalid file format")

    temp_file = f"/tmp/{uuid.uuid4()}.{file_extension}"

    with open(temp_file, "wb") as f:
        f.write(await file.read())

    try:
        schedules = read_excel(temp_file)
    except Exception as e:
        os.remove(temp_file)
        raise HTTPException(status_code=400, detail=str(e))

    if schedules:
        for schedule in schedules:
            schedule["status"] = "pending"
            schedule["created_at"] = datetime.utcnow()
            schedule["sent_at"] = None
        
        result = await database.db.schedules.insert_many(schedules)
        
        for idx, schedule_id in enumerate(result.inserted_ids):
            schedule_email(
                schedule_id=str(schedule_id),
                scheduled_time=schedules[idx]["scheduled_time"],
                timezone_str=schedules[idx]["timezone"]
            )

    os.remove(temp_file)

    return {
        "message": "File uploaded successfully",
        "schedules_added": len(schedules)
    }
