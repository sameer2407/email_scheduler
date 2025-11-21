import pandas as pd
from datetime import datetime

REQUIRED_COLUMNS = ["email", "message", "scheduled_time", "timezone"]


def convert_to_datetime(value):
    if isinstance(value, datetime):
        return value
    
    try:
        return datetime.fromisoformat(str(value))
    except Exception:
        raise Exception(f"Invalid datetime format: {value}")


def read_excel(file_path: str):
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise Exception("Unable to read the Excel file. Make sure the file is valid.") from e
    
    missing = []
    for column in REQUIRED_COLUMNS:
        if column not in df.columns:
            missing.append(column)
    
    if missing:
        raise Exception(f"Missing required columns: {', '.join(missing)}")
    
    schedules = []
    for _, row in df.iterrows():
        try:
            schedule = {
                "email": row["email"],
                "message": row["message"],
                "scheduled_time": convert_to_datetime(row["scheduled_time"]),
                "timezone": row["timezone"]
            }
            schedules.append(schedule)
        except Exception as e:
            raise Exception(f"Error processing row: {e}") from e
    
    return schedules
