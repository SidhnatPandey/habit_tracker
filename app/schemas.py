from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from enum import Enum

class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    class Config:
        orm_mode = True

class HabitBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    frequency: FrequencyEnum
    category_id: int

class HabitCreate(HabitBase):
    pass

class Habit(HabitBase):
    id: int
    class Config:
        orm_mode = True

class HabitCompletionBase(BaseModel):
    date: date
    status: bool

class HabitCompletionCreate(HabitCompletionBase):
    habit_id: int

class HabitCompletion(HabitCompletionBase):
    id: int
    habit_id: int
    class Config:
        orm_mode = True
