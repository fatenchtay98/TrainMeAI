from api import exercise_2
from fastapi import FastAPI
from api import exercise_1

app = FastAPI(title="AI Fitness Trainer")

# Register routers
app.include_router(exercise_1.router, prefix="/exercise_1")
app.include_router(exercise_2.router, prefix="/exercise_2")
