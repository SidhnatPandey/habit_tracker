from fastapi import FastAPI
from . import models, database
from .routes import habits, analytics, categories, completions

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Habit Tracker API",
    description="API for tracking habits, completions, and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/swagger.json"
)


app.include_router(categories.router)
app.include_router(habits.router)
app.include_router(analytics.router)
app.include_router(completions.router)

@app.get("/")
def root():
    return {"message": "Smart Habit Tracker API running"}