from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from .. import crud, database

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/habit/{habit_id}")
def habit_analytics(habit_id: int, start: date, end: date, db: Session = Depends(database.get_db)):
    """
    Example: /analytics/habit/1?start=2025-01-01&end=2025-01-31
    """
    return crud.get_habit_analytics(db, habit_id, start, end)

@router.get("/top")
def top_habits(start: date, end: date, db: Session = Depends(database.get_db)):
    """
    Example: /analytics/top?start=2025-01-01&end=2025-01-31
    """
    return crud.top_3_habits(db, start, end)
