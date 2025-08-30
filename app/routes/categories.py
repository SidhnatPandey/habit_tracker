from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=schemas.Category)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(database.get_db)):
    return crud.create_category(db, category)

@router.get("/", response_model=list[schemas.Category])
def list_categories(db: Session = Depends(database.get_db)):
    return crud.get_categories(db)
