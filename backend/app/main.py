from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from app.database import init_db
from app.routers import api_router

# Load environment variables
load_dotenv()

app = FastAPI(
    title=os.getenv("APP_NAME", "AI Testing Standard Platform"),
    version=os.getenv("APP_VERSION", "1.0.0"),
    description="AI Testing Standard Platform based on Common Criteria"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_db()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to AI Testing Standard Platform",
        "status": "running",
        "version": os.getenv("APP_VERSION", "1.0.0")
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=os.getenv("DEBUG", "True").lower() == "true"
    )
