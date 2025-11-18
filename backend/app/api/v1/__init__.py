"""API v1 routes."""
from fastapi import APIRouter

from app.api.v1 import releases, publishers, metadata

api_router = APIRouter()

api_router.include_router(releases.router, prefix="/releases", tags=["releases"])
api_router.include_router(publishers.router, prefix="/publishers", tags=["publishers"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])
