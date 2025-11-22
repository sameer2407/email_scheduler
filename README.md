# 📧 Email Scheduler

A robust email scheduling backend service built with FastAPI, MongoDB, and APScheduler. Schedule emails to be sent at specific times with timezone support, bulk import from Excel, and integration with external APIs.

## ✨ Features

- 📅 **Schedule Emails** - Send emails at specific times with timezone support
- 📊 **Bulk Import** - Upload Excel files to schedule multiple emails at once
- 🔄 **Public API Integration** - Automatically include posts and optional todo lists from JSONPlaceholder API
- 🌍 **Timezone Support** - Schedule emails in any timezone (UTC, EST, IST, etc.)
- 📝 **RESTful API** - Clean and intuitive API endpoints
- ⚡ **Background Jobs** - APScheduler handles all scheduled tasks
- 🔍 **Status Tracking** - Track email status (pending, sent, failed)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB (local or remote)
- SMTP email account (Gmail recommended)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd email_scheduler
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create `.env` file**
```bash
cp .env.example .env  # If you have an example file, or create manually
```

5. **Configure environment variables**
Create a `.env` file in the root directory:
```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=email_scheduler

# SMTP Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com

# Scheduler Configuration
SCHEDULER_TIMEZONE=UTC
```

6. **Start MongoDB** (if running locally)
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo

# Or use your local MongoDB installation
```

7. **Run the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

### 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 📖 Usage Examples

### Create a Schedule (Postman/cURL)

```bash
POST http://localhost:8000/schedules/
Content-Type: application/json

{
  "email": "recipient@example.com",
  "message": "Your scheduled email message",
  "scheduled_time": "2025-11-23T10:32:00",
  "timezone": "Asia/Kolkata",
  "include_todos": true,
  "user_id": 1
}
```

### Get All Schedules

```bash
GET http://localhost:8000/schedules/

# Filter by status
GET http://localhost:8000/schedules/?status=pending
```

### Upload Excel File

1. Create a sample Excel file:
```bash
python create_sample_excel.py
```

2. Upload via API:
```bash
POST http://localhost:8000/excel/upload
Content-Type: multipart/form-data

file: sample_schedules.xlsx
```

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

Use the interactive API documentation at `http://localhost:8000/docs` to test all endpoints.

Or use Postman/cURL:

```bash
# Health check
curl http://localhost:8000/health

# Create schedule
curl -X POST http://localhost:8000/schedules/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","message":"Test","scheduled_time":"2025-11-23T10:00:00","timezone":"UTC"}'

# Get schedules
curl http://localhost:8000/schedules/
```

## 🐛 Troubleshooting

**MongoDB Connection Error:**
```bash
# Check if MongoDB is running
docker ps | grep mongo

# Check MongoDB logs
docker logs mongodb
```

**Email Not Sending:**
- Verify SMTP credentials in `.env`
- Check that you're using an App Password (not regular password) for Gmail
- Ensure 2FA is enabled on your Gmail account
- Check server logs for error messages

**Scheduler Not Working:**
- Ensure scheduled time is in the future
- Check server logs for scheduler errors
- Verify timezone format is correct (e.g., `Asia/Kolkata`, not `IST`)

## 📝 License

MIT License

## 👤 Author

Your Name

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

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
