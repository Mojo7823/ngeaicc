from fastapi import APIRouter
from .api import router as api_routes

# Main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(api_routes, tags=["api"])
