"""Release repository."""
from datetime import date, datetime
from typing import List, Optional, Dict, Any
from calendar import monthrange

from sqlalchemy import select, func, and_, or_, extract
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import MangaRelease, Publisher
from app.repositories.base import BaseRepository


class ReleaseRepository(BaseRepository[MangaRelease]):
    """Repository for manga releases."""

    def __init__(self, db: AsyncSession):
        super().__init__(MangaRelease, db)

    async def get_current_month_releases(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        publisher_slug: Optional[str] = None,
        region: Optional[str] = None,
        format: Optional[str] = None,
        sort_by: str = "date",
    ) -> tuple[List[MangaRelease], int]:
        """Get releases from the current calendar month."""
        today = date.today()
        first_day = date(today.year, today.month, 1)
        last_day = date(today.year, today.month, monthrange(today.year, today.month)[1])

        return await self._get_releases_in_range(
            start_date=first_day,
            end_date=last_day,
            limit=limit,
            offset=offset,
            publisher_slug=publisher_slug,
            region=region,
            format=format,
            sort_by=sort_by,
        )

    async def get_upcoming_releases(
        self,
        *,
        months: int = 3,
        limit_per_month: int = 100,
        publisher_slug: Optional[str] = None,
        region: Optional[str] = None,
        format: Optional[str] = None,
    ) -> Dict[str, List[MangaRelease]]:
        """Get releases from upcoming months, grouped by month."""
        today = date.today()
        results = {}

        for month_offset in range(1, months + 1):
            # Calculate the target month
            target_month = today.month + month_offset
            target_year = today.year

            while target_month > 12:
                target_month -= 12
                target_year += 1

            first_day = date(target_year, target_month, 1)
            last_day = date(target_year, target_month, monthrange(target_year, target_month)[1])

            releases, _ = await self._get_releases_in_range(
                start_date=first_day,
                end_date=last_day,
                limit=limit_per_month,
                offset=0,
                publisher_slug=publisher_slug,
                region=region,
                format=format,
                sort_by="date",
            )

            month_key = f"{target_year}-{target_month:02d}"
            results[month_key] = releases

        return results

    async def search_releases(
        self,
        *,
        query: str,
        limit: int = 50,
        offset: int = 0,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> tuple[List[MangaRelease], int]:
        """Search releases by title or series name."""
        stmt = select(MangaRelease).options(selectinload(MangaRelease.publisher))

        # Build search conditions
        search_conditions = []
        if query:
            search_term = f"%{query.lower()}%"
            search_conditions.append(
                or_(
                    func.lower(MangaRelease.title).like(search_term),
                    func.lower(MangaRelease.series_name).like(search_term),
                )
            )

        if date_from:
            search_conditions.append(MangaRelease.release_date >= date_from)
        if date_to:
            search_conditions.append(MangaRelease.release_date <= date_to)

        if search_conditions:
            stmt = stmt.where(and_(*search_conditions))

        # Count total
        count_stmt = select(func.count()).select_from(MangaRelease)
        if search_conditions:
            count_stmt = count_stmt.where(and_(*search_conditions))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar_one()

        # Get paginated results
        stmt = stmt.order_by(MangaRelease.release_date.desc())
        stmt = stmt.offset(offset).limit(limit)
        result = await self.db.execute(stmt)
        releases = list(result.scalars().all())

        return releases, total

    async def _get_releases_in_range(
        self,
        *,
        start_date: date,
        end_date: date,
        limit: int,
        offset: int,
        publisher_slug: Optional[str] = None,
        region: Optional[str] = None,
        format: Optional[str] = None,
        sort_by: str = "date",
    ) -> tuple[List[MangaRelease], int]:
        """Get releases in a date range with filters."""
        stmt = select(MangaRelease).options(selectinload(MangaRelease.publisher))

        # Build where conditions
        conditions = [
            MangaRelease.release_date >= start_date,
            MangaRelease.release_date <= end_date,
        ]

        if publisher_slug:
            stmt = stmt.join(Publisher)
            conditions.append(Publisher.slug == publisher_slug)

        if region:
            # Check if region is in the JSON array
            conditions.append(
                func.jsonb_contains(MangaRelease.regions, f'["{region}"]')
            )

        if format:
            conditions.append(MangaRelease.format == format)

        stmt = stmt.where(and_(*conditions))

        # Count total
        count_stmt = select(func.count()).select_from(MangaRelease)
        if publisher_slug:
            count_stmt = count_stmt.join(Publisher)
        count_stmt = count_stmt.where(and_(*conditions))
        count_result = await self.db.execute(count_stmt)
        total = count_result.scalar_one()

        # Apply sorting
        if sort_by == "title":
            stmt = stmt.order_by(MangaRelease.title)
        elif sort_by == "publisher":
            stmt = stmt.join(Publisher).order_by(Publisher.name)
        else:  # default to date
            stmt = stmt.order_by(MangaRelease.release_date)

        # Apply pagination
        stmt = stmt.offset(offset).limit(limit)

        result = await self.db.execute(stmt)
        releases = list(result.scalars().all())

        return releases, total

    async def get_by_isbn(self, isbn_13: str) -> Optional[MangaRelease]:
        """Get release by ISBN-13."""
        result = await self.db.execute(
            select(MangaRelease)
            .options(selectinload(MangaRelease.publisher))
            .where(MangaRelease.isbn_13 == isbn_13)
        )
        return result.scalar_one_or_none()

    async def bulk_upsert(self, releases_data: List[Dict[str, Any]]) -> Dict[str, int]:
        """Bulk upsert releases."""
        created = 0
        updated = 0

        for release_data in releases_data:
            isbn = release_data.get("isbn_13")
            if isbn:
                existing = await self.get_by_isbn(isbn)
                if existing:
                    # Update
                    await self.update(existing.id, **release_data)
                    updated += 1
                else:
                    # Create
                    await self.create(**release_data)
                    created += 1
            else:
                # No ISBN, just create
                await self.create(**release_data)
                created += 1

        await self.db.flush()
        return {"created": created, "updated": updated}
