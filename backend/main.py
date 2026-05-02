from fastapi import FastAPI

from backend.api.routes_generate import router as generate_router
from backend.api.routes_health import router as health_router
from backend.api.routes_scenario import router as scenario_router

app = FastAPI(title="Island Light Generator API", version="0.1.0")

app.include_router(health_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(generate_router, prefix="/api")
