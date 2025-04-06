from api import exercise_2
from fastapi import FastAPI
from api import squat

app = FastAPI(title="AI Fitness Trainer")

# Register routers
app.include_router(squat.router, prefix="/squat")
app.include_router(exercise_2.router, prefix="/exercise_2")
