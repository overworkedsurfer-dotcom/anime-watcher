"""Release API endpoints."""
from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.services.release_service import ReleaseService
from app.config import get_settings

settings = get_settings()
router = APIRouter()


@router.get("/current")
async def get_current_releases(
    limit: int = Query(default=100, ge=1, le=settings.MAX_PAGE_SIZE),
    offset: int = Query(default=0, ge=0),
    publisher: Optional[str] = Query(default=None, description="Publisher slug"),
    region: Optional[str] = Query(default=None, description="Region code (us, uk, etc.)"),
    format: Optional[str] = Query(default=None, description="Format (Paperback, Hardcover, etc.)"),
    sort: str = Query(default="date", regex="^(date|title|publisher)$"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get releases from the current calendar month.

    - **limit**: Number of results (max 100)
    - **offset**: Pagination offset
    - **publisher**: Filter by publisher slug
    - **region**: Filter by region
    - **format**: Filter by format
    - **sort**: Sort by date, title, or publisher
    """
    service = ReleaseService(db)
    return await service.get_current_month_releases(
        limit=limit,
        offset=offset,
        publisher=publisher,
        region=region,
        format=format,
        sort=sort,
    )


@router.get("/upcoming")
async def get_upcoming_releases(
    months: int = Query(default=3, ge=1, le=4),
    publisher: Optional[str] = Query(default=None),
    region: Optional[str] = Query(default=None),
    format: Optional[str] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    Get upcoming releases from the next 3-4 months, grouped by month.

    - **months**: Number of months ahead (1-4)
    - **publisher**: Filter by publisher slug
    - **region**: Filter by region
    - **format**: Filter by format
    """
    service = ReleaseService(db)
    return await service.get_upcoming_releases(
        months=months,
        publisher=publisher,
        region=region,
        format=format,
    )


@router.get("/search")
async def search_releases(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    Search releases by title or series name.

    - **q**: Search query (required)
    - **limit**: Number of results
    - **offset**: Pagination offset
    - **date_from**: Filter by start date
    - **date_to**: Filter by end date
    """
    service = ReleaseService(db)
    return await service.search_releases(
        query=q,
        limit=limit,
        offset=offset,
        date_from=date_from,
        date_to=date_to,
    )
