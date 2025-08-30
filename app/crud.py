from datetime import date
from sqlalchemy.orm import Session
from . import models, schemas
from sqlalchemy import func, desc
from .utils import streaks
from typing import List, Optional
from fastapi import HTTPException


# Category
def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

# Habits
def create_habit(db: Session, habit: schemas.HabitCreate):
    db_habit = models.Habit(**habit.dict())
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

def get_habits(db: Session, skip=0, limit=10):
    return db.query(models.Habit).offset(skip).limit(limit).all()

def get_habit(db: Session, habit_id: int):
    return db.query(models.Habit).filter(models.Habit.id == habit_id).first()

def delete_habit(db: Session, habit_id: int):
    habit = get_habit(db, habit_id)
    if habit:
        db.delete(habit)
        db.commit()
    return habit

# Completions
def mark_completion(db: Session, completion: schemas.HabitCompletionCreate):
    # Check if habit exists before inserting
    habit = db.query(models.Habit).filter(models.Habit.id == completion.habit_id).first()
    if not habit:
        raise HTTPException(status_code=400, detail="Habit does not exist")

    db_completion = models.HabitCompletion(
        habit_id=completion.habit_id,
        date=completion.date,
        status=completion.status
    )
    db.add(db_completion)
    db.commit()
    db.refresh(db_completion)
    return db_completion


def get_habit_analytics(db: Session, habit_id: int, start: date, end: date):
    return {
        "habit_id": habit_id,
        "current_streak": streaks.current_streak(db, habit_id),
        "longest_streak": streaks.longest_streak(db, habit_id),
        "completion_percentage": streaks.completion_percentage(db, habit_id, start, end)
    }

def top_3_habits(db: Session, start: date, end: date):
    results = []
    habits = db.query(models.Habit).all()
    for habit in habits:
        percent = streaks.completion_percentage(db, habit.id, start, end)
        results.append({"habit_id": habit.id, "title": habit.title, "completion_rate": percent})
    return sorted(results, key=lambda x: x["completion_rate"], reverse=True)[:3]

def search_habits(db: Session, keyword: str) -> List[models.Habit]:
    return db.query(models.Habit).filter(
        (models.Habit.title.ilike(f"%{keyword}%")) |
        (models.Habit.description.ilike(f"%{keyword}%"))
    ).all()

def filter_habits(
    db: Session,
    category_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[models.Habit]:
    query = db.query(models.Habit)

    if category_id:
        query = query.filter(models.Habit.category_id == category_id)

    if status:
        if status == "completed":
            query = query.join(models.Habit.completions).filter(models.HabitCompletion.status == True)
        elif status == "pending":
            query = query.join(models.Habit.completions).filter(models.HabitCompletion.status == False)

    return query.all()