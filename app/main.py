from fastapi import FastAPI
from . import models, database
from .routes import habits, analytics, categories, completions

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Smart Habit Tracker")

app.include_router(habits.router)
app.include_router(analytics.router)
app.include_router(categories.router)
app.include_router(completions.router)

@app.get("/")
def root():
    return {"message": "Smart Habit Tracker API running"}