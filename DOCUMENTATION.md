# 📘 API Documentation

Complete API documentation for Email Scheduler service.

## Table of Contents

1. [Base URL](#base-url)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
   - [General Endpoints](#general-endpoints)
   - [Schedule Endpoints](#schedule-endpoints)
   - [Excel Upload](#excel-upload)
4. [Data Models](#data-models)
5. [Error Responses](#error-responses)
6. [Examples](#examples)

---

## Base URL

```
http://localhost:8000
```

For production, replace with your server URL.

---

## Authentication

Currently, the API does not require authentication. In production, you should implement authentication middleware.

---

## General Endpoints

### 1. Root Endpoint

**GET** `/`

Returns API information and status.

**Response:**
```json
{
  "message": "Welcome to Email Scheduler",
  "version": "1.0.0",
  "status": "running"
}
```

**Status Codes:**
- `200 OK` - Success

---

### 2. Health Check

**GET** `/health`

Check if the API is running and healthy.

**Response:**
```json
{
  "status": "healthy"
}
```

**Status Codes:**
- `200 OK` - Service is healthy

---

## Schedule Endpoints

All schedule endpoints are prefixed with `/schedules`.

### 1. Create Schedule

**POST** `/schedules/`

Create a new email schedule.

**Request Body:**
```json
{
  "email": "recipient@example.com",
  "message": "Your email message here",
  "scheduled_time": "2025-11-23T10:32:00",
  "timezone": "Asia/Kolkata",
  "include_todos": false,
  "user_id": 1
}
```

**Fields:**
- `email` (required, string) - Recipient email address (valid email format)
- `message` (required, string) - Email content/body
- `scheduled_time` (required, datetime) - When to send the email (ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`)
- `timezone` (required, string) - Timezone for scheduling (e.g., `UTC`, `Asia/Kolkata`, `America/New_York`)
- `include_todos` (optional, boolean) - Include todos from JSONPlaceholder API (default: `false`)
- `user_id` (optional, integer) - User ID for API integrations - posts and todos (default: `1`, range: 1-10)

**Note:** Posts from JSONPlaceholder API are **automatically included** in all emails based on `user_id`. Todos are only included if `include_todos` is set to `true`.

**Response:**
```json
{
  "id": "692149e5c7e727e7ae3283b0",
  "email": "recipient@example.com",
  "message": "Your email message here",
  "scheduled_time": "2025-11-23T10:32:00",
  "timezone": "Asia/Kolkata",
  "status": "pending",
  "include_todos": false,
  "user_id": 1,
  "created_at": "2025-11-23T08:00:00",
  "sent_at": null
}
```

**Status Codes:**
- `200 OK` - Schedule created successfully
- `422 Unprocessable Entity` - Validation error (invalid data format)

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "message": "Meeting reminder",
    "scheduled_time": "2025-11-23T15:00:00",
    "timezone": "UTC",
    "include_todos": true,
    "user_id": 1
  }'
```

---

### 2. Get All Schedules

**GET** `/schedules/`

Retrieve all schedules, optionally filtered by status.

**Query Parameters:**
- `status` (optional, string) - Filter by status: `pending`, `sent`, or `failed`

**Response:**
```json
[
  {
    "id": "692149e5c7e727e7ae3283b0",
    "email": "user@example.com",
    "message": "Email message",
    "scheduled_time": "2025-11-23T10:32:00",
    "timezone": "Asia/Kolkata",
    "status": "pending",
    "include_todos": false,
    "user_id": 1,
    "created_at": "2025-11-23T08:00:00",
    "sent_at": null
  },
  {
    "id": "692149e5c7e727e7ae3283b1",
    "email": "another@example.com",
    "message": "Another email",
    "scheduled_time": "2025-11-22T12:00:00",
    "timezone": "UTC",
    "status": "sent",
    "include_todos": true,
    "user_id": 2,
    "created_at": "2025-11-22T10:00:00",
    "sent_at": "2025-11-22T12:00:00"
  }
]
```

**Status Codes:**
- `200 OK` - Success

**Examples:**
```bash
# Get all schedules
curl http://localhost:8000/schedules/

# Get only pending schedules
curl http://localhost:8000/schedules/?status=pending

# Get only sent schedules
curl http://localhost:8000/schedules/?status=sent
```

---

### 3. Get Single Schedule

**GET** `/schedules/{schedule_id}`

Retrieve a specific schedule by ID.

**Path Parameters:**
- `schedule_id` (required, string) - MongoDB ObjectId of the schedule

**Response:**
```json
{
  "id": "692149e5c7e727e7ae3283b0",
  "email": "recipient@example.com",
  "message": "Your email message here",
  "scheduled_time": "2025-11-23T10:32:00",
  "timezone": "Asia/Kolkata",
  "status": "pending",
  "include_todos": false,
  "user_id": 1,
  "created_at": "2025-11-23T08:00:00",
  "sent_at": null
}
```

**Status Codes:**
- `200 OK` - Schedule found
- `400 Bad Request` - Invalid schedule ID format
- `404 Not Found` - Schedule not found

**Example:**
```bash
curl http://localhost:8000/schedules/692149e5c7e727e7ae3283b0
```

---

### 4. Update Schedule

**PUT** `/schedules/{schedule_id}`

Update an existing schedule. All fields are optional - only provided fields will be updated.

**Path Parameters:**
- `schedule_id` (required, string) - MongoDB ObjectId of the schedule

**Request Body:**
```json
{
  "email": "newemail@example.com",
  "message": "Updated message",
  "scheduled_time": "2025-11-24T15:00:00",
  "timezone": "America/New_York",
  "status": "pending",
  "include_todos": true,
  "user_id": 2
}
```

**Note:** If `scheduled_time` or `timezone` is updated, the scheduled job will be cancelled and rescheduled.

**Response:**
```json
{
  "id": "692149e5c7e727e7ae3283b0",
  "email": "newemail@example.com",
  "message": "Updated message",
  "scheduled_time": "2025-11-24T15:00:00",
  "timezone": "America/New_York",
  "status": "pending",
  "include_todos": true,
  "user_id": 2,
  "created_at": "2025-11-23T08:00:00",
  "sent_at": null
}
```

**Status Codes:**
- `200 OK` - Schedule updated successfully
- `400 Bad Request` - Invalid schedule ID format
- `404 Not Found` - Schedule not found
- `422 Unprocessable Entity` - Validation error

**Example:**
```bash
curl -X PUT http://localhost:8000/schedules/692149e5c7e727e7ae3283b0 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Updated email message",
    "include_todos": true
  }'
```

---

### 5. Delete Schedule

**DELETE** `/schedules/{schedule_id}`

Delete a schedule and cancel the scheduled email job.

**Path Parameters:**
- `schedule_id` (required, string) - MongoDB ObjectId of the schedule

**Response:**
```json
{
  "message": "Deleted successfully"
}
```

**Status Codes:**
- `200 OK` - Schedule deleted successfully
- `400 Bad Request` - Invalid schedule ID format
- `404 Not Found` - Schedule not found

**Example:**
```bash
curl -X DELETE http://localhost:8000/schedules/692149e5c7e727e7ae3283b0
```

---

## Excel Upload

### Upload Excel File

**POST** `/excel/upload`

Upload an Excel file (`.xlsx` or `.xls`) to bulk create schedules.

**Request:**
- **Content-Type:** `multipart/form-data`
- **Body:** Form data with key `file` containing the Excel file

**Excel File Format:**

| Column | Required | Type | Description |
|--------|----------|------|-------------|
| `email` | ✅ Yes | String | Recipient email address |
| `message` | ✅ Yes | String | Email content |
| `scheduled_time` | ✅ Yes | DateTime | When to send (ISO format: `YYYY-MM-DDTHH:MM:SS`) |
| `timezone` | ✅ Yes | String | Timezone (e.g., `UTC`, `Asia/Kolkata`) |
| `include_todos` | ❌ No | Boolean | Include todos (default: `false`) |
| `user_id` | ❌ No | Integer | User ID for todos (default: `1`) |

**Response:**
```json
{
  "message": "File uploaded successfully",
  "schedules_added": 5
}
```

**Status Codes:**
- `200 OK` - File uploaded and schedules created
- `400 Bad Request` - Invalid file format or missing columns

**Example (cURL):**
```bash
curl -X POST http://localhost:8000/excel/upload \
  -F "file=@sample_schedules.xlsx"
```

**Example (Postman):**
1. Select `POST` method
2. Enter URL: `http://localhost:8000/excel/upload`
3. Go to Body tab
4. Select `form-data`
5. Add key: `file` (type: File)
6. Select your Excel file
7. Send request

**Sample Excel Creation:**
```bash
python create_sample_excel.py
```
This creates a `sample_schedules.xlsx` file with example data.

---

## Data Models

### ScheduleCreate

```typescript
{
  email: string;           // Valid email address (required)
  message: string;         // Email content (required)
  scheduled_time: string;  // ISO 8601 datetime (required)
  timezone: string;        // Timezone string (required)
  include_todos?: boolean; // Include todos from API (optional, default: false)
  user_id?: number;        // User ID for API integrations - posts (always) and todos (optional)
                          // Range: 1-10, default: 1
}
```

**Note:** 
- Posts from JSONPlaceholder API are **automatically included** in all emails based on `user_id`
- Todos are only included when `include_todos: true`

### ScheduleResponse

```typescript
{
  id: string;              // MongoDB ObjectId
  email: string;
  message: string;
  scheduled_time: string;  // ISO 8601 datetime
  timezone: string;
  status: string;          // "pending" | "sent" | "failed"
  include_todos: boolean;
  user_id: number;
  created_at: string;      // ISO 8601 datetime
  sent_at: string | null;  // ISO 8601 datetime or null
}
```

### ScheduleUpdate

All fields are optional:

```typescript
{
  email?: string;
  message?: string;
  scheduled_time?: string;
  timezone?: string;
  status?: string;
  include_todos?: boolean;
  user_id?: number;
}
```

---

## Error Responses

### 400 Bad Request

```json
{
  "detail": "Invalid ID"
}
```

### 404 Not Found

```json
{
  "detail": "Not found"
}
```

### 422 Unprocessable Entity

```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Examples

### Complete Workflow Example

1. **Create a schedule:**
```bash
curl -X POST http://localhost:8000/schedules/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "message": "Daily reminder",
    "scheduled_time": "2025-11-23T10:32:00",
    "timezone": "Asia/Kolkata",
    "include_todos": true,
    "user_id": 1
  }'
```

2. **Get all schedules:**
```bash
curl http://localhost:8000/schedules/
```

3. **Get specific schedule (use ID from step 1):**
```bash
curl http://localhost:8000/schedules/692149e5c7e727e7ae3283b0
```

4. **Update schedule:**
```bash
curl -X PUT http://localhost:8000/schedules/692149e5c7e727e7ae3283b0 \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Updated daily reminder",
    "scheduled_time": "2025-11-23T11:00:00"
  }'
```

5. **Delete schedule:**
```bash
curl -X DELETE http://localhost:8000/schedules/692149e5c7e727e7ae3283b0
```

### Bulk Upload Example

1. **Create sample Excel file:**
```bash
python create_sample_excel.py
```

2. **Upload Excel file:**
```bash
curl -X POST http://localhost:8000/excel/upload \
  -F "file=@sample_schedules.xlsx"
```

---

## Timezone Formats

Use IANA timezone names:

- `UTC`
- `Asia/Kolkata` (Indian Standard Time)
- `America/New_York` (Eastern Time)
- `America/Los_Angeles` (Pacific Time)
- `Europe/London` (GMT/BST)
- `Asia/Tokyo` (JST)
- `Australia/Sydney` (AEDT)

For a complete list, see: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

---

## Public API Integration

The service integrates with [JSONPlaceholder API](https://jsonplaceholder.typicode.com/) to enhance emails with external data. Two types of data can be included:

### Posts API (Always Included)

Posts are **automatically included** in every email based on the `user_id` field. This happens regardless of the `include_todos` setting.

**Posts Format in Email:**
```
Your message here

--- Recent Posts ---
Total Posts: 10

Post 1: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
quia et suscipit
suscipit recusandae consequuntur expedita et cum
reprehenderit molestiae ut ut quas totam...
--------------------------------------------------

Post 2: qui est esse
est rerum tempore vitae
sequi sint nihil reprehenderit dolor ea dolores neque...
--------------------------------------------------

Post 3: ea molestias quasi exercitationem repellat qui ipsa sit aut
et iusto sed quo iure
voluptatem occaecati omnis eligendi aut ad...
--------------------------------------------------

... and 7 more posts
```

**API Endpoint:** `https://jsonplaceholder.typicode.com/posts?userId={user_id}`

**Features:**
- Shows total number of posts for the user
- Displays first 3 posts with title and body preview (truncated to 150 characters)
- Indicates if there are more posts beyond the first 3

### Todos API (Optional)

Todos are included **only when** `include_todos` is set to `true` in the schedule request.

**Todo Summary Format:**
```
Your message here

Your Todo Summary:
Total Tasks: 20
Completed: 11
Pending: 9

Pending Tasks:
1. Task title one
2. Task title two
3. Task title three
4. Task title four
5. Task title five
... and 4 more
```

**API Endpoint:** `https://jsonplaceholder.typicode.com/todos?userId={user_id}`

**Features:**
- Shows total task count
- Displays completed vs pending task counts
- Lists up to 5 pending tasks
- Indicates if there are more pending tasks

### Complete Email Example

When both posts and todos are included:
```
Your scheduled message here

Your Todo Summary:
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

### User ID Usage

The `user_id` field is used for both API integrations:
- **Posts API**: Always fetches posts for the specified `user_id` (default: 1)
- **Todos API**: Fetches todos for the specified `user_id` when `include_todos: true` (default: 1)

Valid `user_id` range: 1-10 (as per JSONPlaceholder API)

---

## Notes

- Scheduled times must be in the future. Past times will not trigger email sending.
- The scheduler automatically starts when the server starts.
- Email status is updated automatically: `pending` → `sent` or `failed`
- All datetime fields use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`
- MongoDB ObjectIds are returned as strings in the API responses
- **Posts are automatically included** in all emails based on `user_id`
- **Todos are optional** and only included when `include_todos: true`
- If API calls fail (network issues, timeout), the email will still be sent without the API data (error is logged)

---

## Interactive Documentation

For interactive testing and documentation, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These provide an interactive interface to test all endpoints without writing code.

