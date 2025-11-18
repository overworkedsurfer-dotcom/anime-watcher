"""Base source protocol."""
from dataclasses import dataclass
from datetime import date
from typing import Protocol, List, Optional


@dataclass
class RawRelease:
    """Raw release data from external source."""

    title: str
    series_name: Optional[str]
    volume_number: Optional[str]
    isbn_13: Optional[str]
    isbn_10: Optional[str]
    release_date: date
    publisher_name: str
    format: Optional[str]
    page_count: Optional[int]
    price_usd: Optional[float]
    price_gbp: Optional[float]
    cover_image_url: Optional[str]
    description: Optional[str]
    demographic: Optional[str]
    genres: List[str]
    regions: List[str]
    authors: List[str]
    illustrators: List[str]
    external_id: str
    source_url: str
    raw_data: dict


class MangaSource(Protocol):
    """Protocol for manga data sources."""

    name: str
    priority: int  # Lower = higher priority

    async def fetch_releases(
        self,
        start_date: date,
        end_date: date,
        *,
        language_filter: str = "en",
        region_filter: Optional[List[str]] = None,
    ) -> List[RawRelease]:
        """Fetch releases from this source."""
        ...

    async def health_check(self) -> bool:
        """Check if source is accessible."""
        ...
