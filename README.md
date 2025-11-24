# 📧 Email Scheduler

[![Python](https://img.shields.io/badge/python-3.12+-3776AB?logo=python&logoColor=fff)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-ready-009688?logo=fastapi&logoColor=fff)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.x-47A248?logo=mongodb&logoColor=fff)](https://www.mongodb.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-000?logo=open-source-initiative&logoColor=fff)](LICENSE)

Email Scheduler is a FastAPI + APScheduler backend that lets teams queue personalized emails, enrich them with JSONPlaceholder posts/todos, and deliver them on precise timezones using MongoDB as a durable job store.

> 🧭 Need to dive deeper? Check `DOCUMENTATION.md` for exhaustive endpoint specs.

## 🗂️ Quick Links

| Section | Purpose |
| --- | --- |
| [Features](#-features) | Core capabilities at a glance |
| [Architecture](#-architecture-overview) | How scheduling, queues, and APIs connect |
| [Setup](#-quick-start) | From clone to running server |
| [Usage](#-usage-examples) | Sample cURL/Postman flows |
| [Excel Format](#-excel-file-format) | Columns for bulk uploads |
| [Troubleshooting](#-troubleshooting) | Self-service fixes |

## ✨ Features

- 📅 **Timezone-aware scheduling** – queue emails in UTC or any IANA timezone
- 📊 **Bulk Excel imports** – convert spreadsheets to schedules in one call
- 🔄 **External enrichment** – attach JSONPlaceholder posts and optional todo summaries
- ⚡ **Reliable background jobs** – APScheduler drives retries and delivery windows
- 🔍 **Status tracking** – surfaces `pending`, `sent`, `failed` states per schedule
- 📝 **Well-documented REST API** – interactive Swagger / ReDoc built-in
- 🔐 **Environment-driven config** – swap SMTP, Mongo, and scheduler settings per deploy

## 🏗️ Architecture Overview

```
Client (Swagger, Postman, Excel uploader)
        │
FastAPI routes (`/schedules`, `/excel/upload`)
        │
MongoDB (schedule store) ── APScheduler (jobs & triggers)
        │                                   │
Public API service (posts/todos)     Email sender (SMTP)
```

- **FastAPI** handles validation, routing, and OpenAPI generation.
- **MongoDB** persists schedules and doubles as APScheduler's backing store.
- **APScheduler** runs in-process and wakes up according to the configured timezone.
- **Email services** build payloads, run optional formatting (todos/posts), and push to SMTP.

## 🧰 Tech Stack

- FastAPI, Starlette, Pydantic v2
- APScheduler for cron-like trigger management
- MongoDB / MongoDB Atlas for persistence
- Requests for public API enrichment
- OpenPyXL + pandas utilities for Excel ingestion

## 🚀 Quick Start

### Prerequisites

- Python 3.10+ (3.12 recommended)
- MongoDB (local Docker container or Atlas cluster)
- SMTP inbox (Gmail works well when using an App Password)

### 1. Clone & bootstrap

```bash
git clone <your-repo-url>
cd email_scheduler
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

Create `.env` in the repo root:

```env
# MongoDB: choose local or Atlas
MONGODB_URL=mongodb://localhost:27017
# or MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/email_scheduler
DATABASE_NAME=email_scheduler

# SMTP (Gmail example)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

# Scheduler defaults
SCHEDULER_TIMEZONE=UTC
```

Need sample data? Run `python create_sample_excel.py` to generate `sample_schedules.xlsx`.

#### Local Mongo using Docker

```bash
docker run -d --name mongodb -p 27017:27017 mongo:7
```

#### MongoDB Atlas (recommended for prod)

1. Create an Atlas cluster (M0 is free).
2. Add a database user and IP allowlist.
3. Paste the SRV URI (starts with `mongodb+srv://`) into `MONGODB_URL`.
4. Keep `DATABASE_NAME=email_scheduler`.

Atlas URIs automatically trigger ServerApi v1 in the driver; localhost URIs use the standard client.

### 3. Run the API

```bash
uvicorn app.main:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/health`

Application logs show whether the connection type is **Local MongoDB** or **MongoDB Atlas** at startup.

### 4. Optional development helpers

- `uvicorn app.main:app --reload --port 9000` – run on a custom port
- `ENV_FILE=.env.staging uvicorn app.main:app` – point to alternate env files (via shell export)

## 📖 Usage Examples

### Create a schedule

```bash
curl -X POST http://localhost:8000/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "recipient@example.com",
    "message": "Your scheduled email message",
    "scheduled_time": "2025-11-23T10:32:00",
    "timezone": "Asia/Kolkata",
    "include_todos": true,
    "user_id": 1
  }'
```

### Filter schedules by status

```bash
curl "http://localhost:8000/schedules/?status=pending"
```

### Upload Excel file

```bash
python create_sample_excel.py            # generates sample_schedules.xlsx
curl -X POST http://localhost:8000/excel/upload \
  -F "file=@sample_schedules.xlsx"
```

The upload endpoint validates headers, datatypes, and timezone strings before committing jobs into MongoDB.

## 📋 Excel File Format

Your Excel file should have these columns:

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| `email` | ✅ Yes | String | Recipient email address |
| `message` | ✅ Yes | String | Email content |
| `scheduled_time` | ✅ Yes | DateTime | When to send (ISO format: YYYY-MM-DDTHH:MM:SS) |
| `timezone` | ✅ Yes | String | Timezone (e.g., UTC, Asia/Kolkata, America/New_York) |
| `include_todos` | ❌ No | Boolean | Include todos from API (default: false) |
| `user_id` | ❌ No | Integer | User ID for API integrations - todos and posts (default: 1, range: 1-10) |

## 🔧 Gmail Setup

To use Gmail as your SMTP server:

1. **Enable 2-Factor Authentication** on your Google account
2. **Generate App Password**:
   - Go to: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the generated password
3. **Use the App Password** in your `.env` file (not your regular password)

## 🏗️ Project Structure

```
email_scheduler/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── database.py          # MongoDB connection
│   ├── models/
│   │   └── schedule_model.py    # Pydantic models
│   ├── routes/
│   │   ├── schedule_routes.py   # Schedule CRUD endpoints
│   │   └── excel_routes.py      # Excel upload endpoint
│   ├── services/
│   │   ├── scheduler.py         # APScheduler integration
│   │   ├── email_sender.py      # SMTP email sending
│   │   ├── public_api.py        # External API integration
│   │   └── weather_api.py       # Weather API (if used)
│   └── utils/
│       └── excel_reader.py      # Excel file parser
├── create_sample_excel.py   # Utility to create sample Excel file
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── DOCUMENTATION.md        # Detailed API documentation
└── .gitignore             # Git ignore rules
```

## 🧭 Deployment Checklist

- [ ] Configure `MONGODB_URL`, `DATABASE_NAME`, and SMTP secrets via environment manager (Docker secrets, GitHub Actions, etc.).
- [ ] Enable HTTPS termination in your reverse proxy (Traefik, Nginx, Caddy).
- [ ] Set `SCHEDULER_TIMEZONE` to the primary business timezone or `UTC`.
- [ ] Turn on structured logging (e.g., `uvicorn --log-config logging.ini`) if you need JSON logs.
- [ ] Configure process supervision (systemd, Docker, PM2) to auto-restart the API.
- [ ] Monitor `/health` with your uptime checker.

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Root endpoint - API info |
| GET | `/health` | Health check |
| POST | `/schedules/` | Create new schedule |
| GET | `/schedules/` | Get all schedules (optional status filter) |
| GET | `/schedules/{id}` | Get single schedule |
| PUT | `/schedules/{id}` | Update schedule |
| DELETE | `/schedules/{id}` | Delete schedule |
| POST | `/excel/upload` | Upload Excel file for bulk scheduling |

## 🔍 Schedule Status

- `pending` - Scheduled, not yet sent
- `sent` - Successfully delivered
- `failed` - Failed to send

## 🧪 Testing

- **Interactive** – open `http://localhost:8000/docs`, authorize if needed, and send requests directly from Swagger UI.
- **Smoke tests** – run the three cURL snippets below after every deployment:

```bash
curl http://localhost:8000/health
curl http://localhost:8000/schedules/
curl -X POST http://localhost:8000/schedules/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","message":"Test","scheduled_time":"2025-11-23T10:00:00","timezone":"UTC"}'
```

- **Excel ingestion** – execute `python create_sample_excel.py` and upload the generated file to ensure bulk imports still work after schema changes.
- **Background worker** – verify that cron jobs fire by creating a schedule a few minutes out and confirming the logs/SMTP inbox.

## 📊 Monitoring & Observability

- `/health` – lightweight readiness probe.
- MongoDB + APScheduler logs include job IDs and state transitions; ship them to your log stack of choice.
- Add alerting on `failed` schedules via a MongoDB change stream or a periodic analytics job if you need proactive paging.
- Consider wrapping `email_sender.send_email` with metrics (Prometheus, StatsD) for delivery counts and latency tracking.

## 🐛 Troubleshooting

| Symptom | Checks |
| --- | --- |
| Cannot connect to MongoDB | `docker ps | grep mongo`, inspect `docker logs mongodb`, confirm connection string matches SRV/local format |
| Emails stuck in `pending` | Confirm SMTP credentials, use Gmail App Password, ensure port 587 is open, check server logs for `smtplib` errors |
| Scheduler never fires | Verify target time is in the future, confirm `SCHEDULER_TIMEZONE`, ensure server clock/timezone is correct |
| Excel upload fails | Make sure headers match the table below exactly, ensure `scheduled_time` is ISO-like (`2025-11-23T10:00:00`), confirm booleans are `true/false` |
| JSONPlaceholder data missing | Service is rate-limited occasionally—logs will show warning but emails still send; retry later or cache results |

## 📝 License

MIT License

## 👤 Author

Sameer

## 🤝 Contributing

1. Fork the repo and create a feature branch (`git checkout -b feat/my-change`).
2. Add or update documentation alongside your code changes.
3. Ensure the API boots locally (`uvicorn app.main:app --reload`) and basic smoke tests pass.
4. Open a pull request describing motivation, screenshots/logs, and manual test notes.

## 🔗 Public API Integration

The service integrates with [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) to enhance emails:

### Posts API (Always Included)
- **Automatically included** in every email based on `user_id`
- Fetches posts from: `https://jsonplaceholder.typicode.com/posts?userId={user_id}`
- Displays total posts count and first 3 posts with title and body preview

### Todos API (Optional)
- **Optionally included** when `include_todos: true` is set
- Fetches todos from: `https://jsonplaceholder.typicode.com/todos?userId={user_id}`
- Displays task summary with completed/pending counts and pending tasks list

**Example Email Format:**
```
Your scheduled message here

Your Todo Summary: (if include_todos is true)
Total Tasks: 20
Completed: 11
Pending: 9
Pending Tasks:
1. Task one
2. Task two
...

--- Recent Posts ---
Total Posts: 10

Post 1: Post Title
Post body preview...
--------------------------------------------------

Post 2: Another Post Title
Another post body preview...
--------------------------------------------------
...
```

## 📄 See Also

- [DOCUMENTATION.md](DOCUMENTATION.md) - Detailed API documentation
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [APScheduler Documentation](https://apscheduler.readthedocs.io/)
- [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) - Public API for testing
