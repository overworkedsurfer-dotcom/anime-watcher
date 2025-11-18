"""Release schemas."""
from datetime import date
from typing import List, Optional, Dict
from decimal import Decimal

from pydantic import BaseModel, Field


class PublisherSchema(BaseModel):
    """Publisher schema."""

    id: int
    name: str
    slug: str
    country: Optional[str] = None

    class Config:
        from_attributes = True


class MangaReleaseSchema(BaseModel):
    """Manga release schema."""

    id: int
    title: str
    series_name: Optional[str] = None
    volume_number: Optional[str] = None
    isbn_13: Optional[str] = None
    isbn_10: Optional[str] = None
    release_date: date
    publisher: PublisherSchema
    format: Optional[str] = None
    page_count: Optional[int] = None
    price_usd: Optional[Decimal] = None
    price_gbp: Optional[Decimal] = None
    cover_image_url: Optional[str] = None
    description: Optional[str] = None
    demographic: Optional[str] = None
    genres: List[str] = Field(default_factory=list)
    regions: List[str] = Field(default_factory=list)
    authors: List[str] = Field(default_factory=list)
    illustrators: List[str] = Field(default_factory=list)

    class Config:
        from_attributes = True


class PaginationMeta(BaseModel):
    """Pagination metadata."""

    total: int
    limit: int
    offset: int


class MangaReleaseListResponse(BaseModel):
    """Response for current month releases."""

    data: List[MangaReleaseSchema]
    meta: Dict


class UpcomingReleasesResponse(BaseModel):
    """Response for upcoming releases grouped by month."""

    data: Dict[str, List[MangaReleaseSchema]]
    meta: Dict


class SearchResponse(BaseModel):
    """Response for search results."""

    data: List[MangaReleaseSchema]
    meta: Dict


class PublisherFilterSchema(BaseModel):
    """Publisher filter option."""

    id: int
    name: str
    slug: str
    release_count: int = 0


class MetadataFiltersResponse(BaseModel):
    """Available filter options."""

    publishers: List[PublisherFilterSchema]
    regions: List[str]
    formats: List[str]
    demographics: List[str]
    genres: List[str]
