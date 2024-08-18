from fastapi import APIRouter

from app.api.v1 import stars, constellations

api_router = APIRouter()
api_router.include_router(stars.router, prefix="/star", tags=["stars"])
api_router.include_router(constellations.router, prefix="/constellation", tags=["constellations"])
