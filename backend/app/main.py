from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib
import os
from contextlib import asynccontextmanager
from app.config import settings
from app.database import engine, Base
from app.routes.auth import router as auth_router
from app.routes.prediction import router as prediction_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load machine learning model once
    model_path = settings.MODEL_PATH
    print(f"Loading machine learning model from {model_path}...")
    if not os.path.exists(model_path):
        # Fallback to current working directory checking if run from within app/
        alt_path = os.path.join(os.path.dirname(__file__), "ml", "upi_fraud_model.pkl")
        if os.path.exists(alt_path):
            model_path = alt_path
        else:
            raise FileNotFoundError(f"Model file not found at {model_path}. Make sure it is copied correctly.")
            
    app.state.model = joblib.load(model_path)
    print("Machine learning model loaded successfully.")
    
    # Initialize Database Tables
    print("Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables initialized successfully.")
    
    yield
    
    # Shutdown
    print("Shutting down application...")

app = FastAPI(
    title="UPI Fraud Detection System API",
    description="FastAPI Backend for detecting fraudulent UPI transactions using a pre-trained ML model.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration — allow all origins for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.responses import FileResponse

# Include API routers under /api prefix
app.include_router(auth_router, prefix="/api")
app.include_router(prediction_router, prefix="/api")

@app.get("/")
def read_root():
    index_path = os.path.join(os.path.dirname(__file__), "..", "..", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {
        "status": "healthy",
        "message": "UPI Fraud Guard API is active. Access docs at /docs"
    }

@app.get("/index-2.html")
def read_index_2():
    index_path = os.path.join(os.path.dirname(__file__), "..", "..", "index-2.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index-2.html not found"}

