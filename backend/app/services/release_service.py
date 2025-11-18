"""Release service."""
from datetime import date
from typing import List, Optional, Dict, Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.release_repository import ReleaseRepository
from app.repositories.publisher_repository import PublisherRepository
from app.schemas.release import MangaReleaseSchema, PublisherSchema
from app.services.cache_service import cache_service
from app.config import get_settings

settings = get_settings()


class ReleaseService:
    """Service for managing manga releases."""

    def __init__(self, db: AsyncSession):
        """Initialize service."""
        self.release_repo = ReleaseRepository(db)
        self.publisher_repo = PublisherRepository(db)

    async def get_current_month_releases(
        self,
        *,
        limit: int = 100,
        offset: int = 0,
        publisher: Optional[str] = None,
        region: Optional[str] = None,
        format: Optional[str] = None,
        sort: str = "date",
    ) -> Dict[str, Any]:
        """Get current month releases with caching."""
        # Build cache key
        cache_key = f"releases:current:{limit}:{offset}:{publisher}:{region}:{format}:{sort}"

        # Try cache first
        cached = await cache_service.get(cache_key)
        if cached:
            return cached

        # Fetch from database
        releases, total = await self.release_repo.get_current_month_releases(
            limit=limit,
            offset=offset,
            publisher_slug=publisher,
            region=region,
            format=format,
            sort_by=sort,
        )

        # Build response
        today = date.today()
        response = {
            "data": [self._release_to_schema(r) for r in releases],
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "month": f"{today.year}-{today.month:02d}",
            },
        }

        # Cache the response
        await cache_service.set(cache_key, response, ttl=settings.CACHE_CURRENT_MONTH)

        return response

    async def get_upcoming_releases(
        self,
        *,
        months: int = 3,
        publisher: Optional[str] = None,
        region: Optional[str] = None,
        format: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get upcoming releases grouped by month."""
        # Build cache key
        cache_key = f"releases:upcoming:{months}:{publisher}:{region}:{format}"

        # Try cache first
        cached = await cache_service.get(cache_key)
        if cached:
            return cached

        # Fetch from database
        releases_by_month = await self.release_repo.get_upcoming_releases(
            months=months,
            publisher_slug=publisher,
            region=region,
            format=format,
        )

        # Build response
        response_data = {}
        total = 0
        for month_key, releases in releases_by_month.items():
            response_data[month_key] = [self._release_to_schema(r) for r in releases]
            total += len(releases)

        response = {
            "data": response_data,
            "meta": {
                "total": total,
                "months_covered": list(releases_by_month.keys()),
            },
        }

        # Cache the response
        await cache_service.set(cache_key, response, ttl=settings.CACHE_UPCOMING_MONTHS)

        return response

    async def search_releases(
        self,
        *,
        query: str,
        limit: int = 50,
        offset: int = 0,
        date_from: Optional[date] = None,
        date_to: Optional[date] = None,
    ) -> Dict[str, Any]:
        """Search releases."""
        # Build cache key
        cache_key = f"releases:search:{query}:{limit}:{offset}:{date_from}:{date_to}"

        # Try cache first
        cached = await cache_service.get(cache_key)
        if cached:
            return cached

        # Search database
        releases, total = await self.release_repo.search_releases(
            query=query,
            limit=limit,
            offset=offset,
            date_from=date_from,
            date_to=date_to,
        )

        # Build response
        response = {
            "data": [self._release_to_schema(r) for r in releases],
            "meta": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "query": query,
            },
        }

        # Cache the response
        await cache_service.set(cache_key, response, ttl=settings.CACHE_SEARCH)

        return response

    async def get_metadata_filters(self) -> Dict[str, Any]:
        """Get available filter options."""
        cache_key = "metadata:filters"

        # Try cache first
        cached = await cache_service.get(cache_key)
        if cached:
            return cached

        # Get publishers with counts
        publishers = await self.publisher_repo.get_all_with_release_count()

        # Build response with common values
        response = {
            "publishers": publishers,
            "regions": ["us", "uk", "ca", "au"],
            "formats": ["Paperback", "Hardcover", "Digital"],
            "demographics": ["Shonen", "Shojo", "Seinen", "Josei", "Kodomo"],
            "genres": [
                "Action", "Adventure", "Comedy", "Drama", "Fantasy",
                "Horror", "Mystery", "Romance", "Sci-Fi", "Slice of Life",
                "Sports", "Supernatural", "Thriller", "Historical"
            ],
        }

        # Cache the response
        await cache_service.set(cache_key, response, ttl=settings.CACHE_METADATA)

        return response

    def _release_to_schema(self, release) -> dict:
        """Convert release model to schema dict."""
        return {
            "id": release.id,
            "title": release.title,
            "series_name": release.series_name,
            "volume_number": release.volume_number,
            "isbn_13": release.isbn_13,
            "isbn_10": release.isbn_10,
            "release_date": release.release_date.isoformat(),
            "publisher": {
                "id": release.publisher.id,
                "name": release.publisher.name,
                "slug": release.publisher.slug,
                "country": release.publisher.country,
            },
            "format": release.format,
            "page_count": release.page_count,
            "price_usd": float(release.price_usd) if release.price_usd else None,
            "price_gbp": float(release.price_gbp) if release.price_gbp else None,
            "cover_image_url": release.cover_image_url,
            "description": release.description,
            "demographic": release.demographic,
            "genres": release.genres or [],
            "regions": release.regions or [],
            "authors": release.authors or [],
            "illustrators": release.illustrators or [],
        }
