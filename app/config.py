import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    APP_NAME = "Email Scheduler"
    VERSION = "1.0.0"
    
    MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "email_scheduler")
    
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", "")
    
    UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/tmp")
    SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "UTC")


settings = Settings()
