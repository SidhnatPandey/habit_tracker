
from sqlalchemy import Boolean, Column, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Base
import enum

class FrequencyEnum(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    habits = relationship("Habit", back_populates="category")

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    start_date = Column(Date)   # ✅ Must match schemas.py
    frequency = Column(Enum(FrequencyEnum))
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="habits")
    completions = relationship("HabitCompletion", back_populates="habit")


class HabitCompletion(Base):
    __tablename__ = "habit_completions"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"))
    date = Column(Date)
    status = Column(Boolean, default=False)

    habit = relationship("Habit", back_populates="completions")
    