"""Publisher API endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.repositories.publisher_repository import PublisherRepository

router = APIRouter()


@router.get("")
async def get_publishers(
    db: AsyncSession = Depends(get_db),
):
    """
    Get all publishers with their release count.
    """
    repo = PublisherRepository(db)
    publishers = await repo.get_all_with_release_count()
    return {"data": publishers}
