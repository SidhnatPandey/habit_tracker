# 📌 Smart Habit Tracker

A **Habit Tracker API** built with **FastAPI** and **PostgreSQL**.  
It allows users to manage habits, mark completions, track streaks, and generate analytics reports.

---

## 🚀 Features

### ✅ Core
- Add, update, delete habits  
- Mark habit completions (daily/weekly)  
- Categorize habits (health, learning, productivity, etc.)  
- Search & filter habits  

### 📊 Analytics
- Current streak (consecutive days)  
- Longest streak  
- Completion percentage over a period  
- Top 3 habits by completion rate  

### 🧩 Optional
- Suggest weakest habit (lowest completion rate)  
- Generate weekly summary report (console or file)  

---

## 🛠️ Tech Stack
- [FastAPI](https://fastapi.tiangolo.com/) – API framework  
- [PostgreSQL](https://www.postgresql.org/) – Relational database  
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM  
- [Pydantic v2](https://docs.pydantic.dev/latest/) – Data validation  
- [Uvicorn](https://www.uvicorn.org/) – ASGI server  

---

## 📂 Project Structure

```
habit-tracker/
│── app/
│   ├── main.py           # FastAPI entrypoint
│   ├── database.py       # DB connection
│   ├── models.py         # SQLAlchemy models
│   ├── schemas.py        # Pydantic schemas
│   ├── crud.py           # DB queries
│   ├── routes/           # API routes
│   │   ├── habits.py
│   │   ├── analytics.py
│   │   └── categories.py
│   └── utils/            # Helper functions
│       └── streaks.py
│── requirements.txt
│── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/SidhnatPandey/habit_tracker.git
cd habit-tracker
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Setup PostgreSQL
1. Make sure PostgreSQL is running.
2. Create database:
   ```sql
   CREATE DATABASE habitdb;
   ```
3. Update DB URL inside `.env` (or `database.py` if hardcoded).

---

## 🔑 Environment Variables (`.env`)
Create a `.env` file in project root:

```ini
DATABASE_URL=postgresql://postgres:yourpassword@localhost:5432/habitdb
```

Update `database.py` to load it:

```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
```

---

## ▶️ Run the Project
```bash
uvicorn app.main:app --reload
```

API will be available at:  
👉 [http://127.0.0.1:8000](http://127.0.0.1:8000)  

Swagger docs:  
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

---

## 🧪 Sample API Usage

### ➕ Add a habit
```http
POST /habits/
{
  "title": "Morning Jog",
  "description": "Run 2km",
  "start_date": "2025-01-01",
  "frequency": "daily",
  "category_id": 1
}
```

### ✅ Mark completion
```http
POST /completions/
{
  "habit_id": 1,
  "date": "2025-01-02",
  "status": true
}
```

### 📊 Analytics for a habit
```
GET /analytics/habit/1?start=2025-01-01&end=2025-01-31
```

Response:
```json
{
  "habit_id": 1,
  "current_streak": 3,
  "longest_streak": 7,
  "completion_percentage": 80.0
}
```

---

## 📝 Assumptions
- Frequency supports only **daily** or **weekly**.  
- Streaks are calculated based on consecutive days with `status=true`.  
- Categories must be created before assigning to habits.  

---

## 📌 Future Improvements
- User authentication  
- Frontend (React/Angular)  
- Notifications & reminders  
