"""Metadata API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.services.release_service import ReleaseService

router = APIRouter()


@router.get("/filters")
async def get_filters(
    db: AsyncSession = Depends(get_db),
):
    """
    Get available filter options for publishers, regions, formats, etc.
    """
    service = ReleaseService(db)
    return await service.get_metadata_filters()
