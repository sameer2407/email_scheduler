import pandas as pd
from datetime import datetime, timedelta


def create_sample_excel(filename="sample_schedules.xlsx"):
    time_1 = (datetime.utcnow() + timedelta(hours=1)).strftime("%Y-%m-%dT%H:%M:%S")
    time_2 = (datetime.utcnow() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S")
    time_3 = (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    
    data = {
        "email": [
            "user1@example.com",
            "user2@example.com",
            "user3@example.com",
            "user4@example.com"
        ],
        "message": [
            "Hello! Your first scheduled email.",
            "Meeting reminder for tomorrow.",
            "Weekly report is ready.",
            "Don't forget your tasks!"
        ],
        "scheduled_time": [
            time_1,
            time_2,
            time_3,
            time_1
        ],
        "timezone": [
            "UTC",
            "America/New_York",
            "Europe/London",
            "Asia/Tokyo"
        ],
        "include_todos": [
            True,
            True,
            False,
            True
        ],
        "user_id": [
            1,
            2,
            1,
            3
        ]
    }
    
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    
    print(f"Created: {filename}")
    print(f"\nSchedules: {len(df)}")
    print(df.to_string(index=False))
    print(f"\nUpload via: POST /excel/upload")


if __name__ == "__main__":
    create_sample_excel()

