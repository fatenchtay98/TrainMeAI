from fastapi import FastAPI

from api import squat
from api import lateral_raise

app = FastAPI(title="AI Fitness Trainer")

# Register routers
app.include_router(squat.router, prefix="/squat")
app.include_router(lateral_raise.router, prefix="/lateral")
