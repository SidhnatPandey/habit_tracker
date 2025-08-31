from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/habits", tags=["Habits"])

# Create Habit
@router.post("/", response_model=schemas.Habit)
def create_habit(habit: schemas.HabitCreate, db: Session = Depends(database.get_db)):
    return crud.create_habit(db, habit)

# List Habits
@router.get("/", response_model=list[schemas.Habit])
def list_habits(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    return crud.get_habits(db, skip, limit)

# Delete Habit
@router.delete("/{habit_id}", response_model=schemas.Habit)
def delete_habit(habit_id: int, db: Session = Depends(database.get_db)):
    return crud.delete_habit(db, habit_id)

# Search Habits
@router.get("/search", response_model=list[schemas.Habit])
def search_habits(keyword: str = Query(..., description="Search by title or description"), 
                  db: Session = Depends(database.get_db)):
    return crud.search_habits(db, keyword)

# Filter Habits
@router.get("/filter", response_model=list[schemas.Habit])
def filter_habits(category_id: int = None, status: str = None, db: Session = Depends(database.get_db)):
    """
    status = completed | pending
    """
    return crud.filter_habits(db, category_id, status)
