from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from backend.api.routes_generate import router as generate_router
from backend.api.routes_health import router as health_router
from backend.api.routes_scenario import router as scenario_router

app = FastAPI(title="Island Light Generator API", version="0.1.0")

load_dotenv() # 載入 backend/.env

# 從 .env 讀取允許的來源
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # 允許來源
    allow_credentials=True,
    allow_methods=["*"],            # 允許所有方法 (GET, POST 等)
    allow_headers=["*"],            # 允許所有標頭
)

app.include_router(health_router, prefix="/api")
app.include_router(scenario_router, prefix="/api")
app.include_router(generate_router, prefix="/api")
