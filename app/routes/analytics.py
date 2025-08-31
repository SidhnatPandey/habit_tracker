# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from datetime import date
# from .. import crud, database

# router = APIRouter(prefix="/analytics", tags=["Analytics"])

# @router.get("/habit/{habit_id}")
# def habit_analytics(habit_id: int, start: date, end: date, db: Session = Depends(database.get_db)):
#     """
#     Example: /analytics/habit/1?start=2025-01-01&end=2025-01-31
#     """
#     return crud.get_habit_analytics(db, habit_id, start, end)

# @router.get("/top")
# def top_habits(start: date, end: date, db: Session = Depends(database.get_db)):
#     """
#     Example: /analytics/top?start=2025-01-01&end=2025-01-31
#     """
#     return crud.top_3_habits(db, start, end)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, database
from datetime import date, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Current Streak
@router.get("/{habit_id}/current-streak")
def get_current_streak(habit_id: int, db: Session = Depends(get_db)):
    completions = db.query(models.HabitCompletion).filter(
        models.HabitCompletion.habit_id == habit_id,
        models.HabitCompletion.status == True
    ).order_by(models.HabitCompletion.date.desc()).all()

    if not completions:
        return {"habit_id": habit_id, "current_streak": 0}

    streak = 0
    today = date.today()
    for c in completions:
        if c.date == today - timedelta(days=streak):
            streak += 1
        else:
            break

    return {"habit_id": habit_id, "current_streak": streak}


# Longest Streak
@router.get("/{habit_id}/longest-streak")
def get_longest_streak(habit_id: int, db: Session = Depends(get_db)):
    completions = db.query(models.HabitCompletion).filter(
        models.HabitCompletion.habit_id == habit_id,
        models.HabitCompletion.status == True
    ).order_by(models.HabitCompletion.date).all()

    if not completions:
        return {"habit_id": habit_id, "longest_streak": 0}

    longest, current = 1, 1
    for i in range(1, len(completions)):
        prev = completions[i - 1].date
        curr = completions[i].date
        if curr == prev + timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    return {"habit_id": habit_id, "longest_streak": longest}


# Completion Percentage
@router.get("/{habit_id}/completion-percentage")
def get_completion_percentage(habit_id: int, start: date, end: date, db: Session = Depends(get_db)):
    total_days = (end - start).days + 1
    if total_days <= 0:
        raise HTTPException(status_code=400, detail="Invalid date range")

    completions = db.query(models.HabitCompletion).filter(
        models.HabitCompletion.habit_id == habit_id,
        models.HabitCompletion.date >= start,
        models.HabitCompletion.date <= end,
        models.HabitCompletion.status == True
    ).count()

    percentage = (completions / total_days) * 100
    return {
        "habit_id": habit_id,
        "start": start,
        "end": end,
        "completion_percentage": round(percentage, 2)
    }


# Top 3 Habits by Completion Rate
@router.get("/top-habits")
def get_top_habits(db: Session = Depends(get_db)):
    habits = db.query(models.Habit).all()
    results = []

    for habit in habits:
        total = db.query(models.HabitCompletion).filter(
            models.HabitCompletion.habit_id == habit.id
        ).count()
        completed = db.query(models.HabitCompletion).filter(
            models.HabitCompletion.habit_id == habit.id,
            models.HabitCompletion.status == True
        ).count()

        rate = (completed / total * 100) if total > 0 else 0
        results.append({
            "habit_id": habit.id,
            "title": habit.title,
            "completion_rate": round(rate, 2)
        })

    top_habits = sorted(results, key=lambda x: x["completion_rate"], reverse=True)[:3]
    return {"top_habits": top_habits}
