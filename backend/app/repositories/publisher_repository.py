"""Publisher repository."""
from typing import List, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Publisher, MangaRelease
from app.repositories.base import BaseRepository


class PublisherRepository(BaseRepository[Publisher]):
    """Repository for publishers."""

    def __init__(self, db: AsyncSession):
        super().__init__(Publisher, db)

    async def get_by_slug(self, slug: str) -> Optional[Publisher]:
        """Get publisher by slug."""
        result = await self.db.execute(
            select(Publisher).where(Publisher.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_all_with_release_count(self) -> List[dict]:
        """Get all publishers with their release count."""
        stmt = (
            select(
                Publisher.id,
                Publisher.name,
                Publisher.slug,
                func.count(MangaRelease.id).label("release_count")
            )
            .outerjoin(MangaRelease, Publisher.id == MangaRelease.publisher_id)
            .group_by(Publisher.id)
            .order_by(Publisher.name)
        )

        result = await self.db.execute(stmt)
        return [
            {
                "id": row.id,
                "name": row.name,
                "slug": row.slug,
                "release_count": row.release_count or 0,
            }
            for row in result.all()
        ]

    async def get_or_create(self, name: str, slug: str, **kwargs) -> Publisher:
        """Get existing publisher or create a new one."""
        existing = await self.get_by_slug(slug)
        if existing:
            return existing

        return await self.create(name=name, slug=slug, **kwargs)
