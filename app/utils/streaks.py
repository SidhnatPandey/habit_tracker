from datetime import date, timedelta
from sqlalchemy.orm  import Session
from .. import models


def current_streak(db: Session, habit_id: int) -> int:
    completions = (
        db.query(models.HabitCompletion).filter(models.HabitCompletion.habit_id == habit_id, models.HabitCompletion.status == True)
        .order_by(models.HabitCompletion.date.desc()).all()
    )

    if not completions:
        return 0
    
    streak = 0
    today = date.today()

    for comp in completions:
        if comp.date == today - timedelta(days=streak):
            streak += 1
        else:
            break
    
    return streak

def longest_streak(db: Session, habit_id: int) -> int:
    completions = (
        db.query(models.HabitCompletion).filter(models.HabitCompletion.habit_id == habit_id, models.HabitCompletion.status == True).order_by(models.HabitCompletion.date).all()
    )

    if not completions:
        return 0
    
    longest, current = 1, 1
    for i in range(1, len(completions)):
        if (completions[i].date - completions[i - 1].date).days == 1:
            current += 1
        else: 
            longest = max(longest, current)
            current = 1
    return max(longest, current)

def completion_percentage(db: Session, habit_id: int, start: date, end: date) -> float:
    total_days = (end - start).days + 1
    completed_days = (
        db.query(models.HabitCompletion).filter(
            models.HabitCompletion.habit_id == habit_id,
            models.HabitCompletion.status == True,
            models.HabitCompletion.date.between(start, end)
        ).count()
    )
    return round((completed_days / total_days) * 100, 2) if total_days > 0 else 0.0