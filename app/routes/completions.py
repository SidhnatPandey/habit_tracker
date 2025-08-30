from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/completions", tags=["Completions"])

@router.post("/", response_model=schemas.HabitCompletion)
def mark_completion(completion: schemas.HabitCompletionCreate, db: Session = Depends(database.get_db)):
    return crud.mark_completion(db, completion)
