"""Release models."""
from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Numeric, Text, JSON
from sqlalchemy.orm import relationship

from app.utils.database import Base


class MangaRelease(Base):
    """Manga release model."""

    __tablename__ = "manga_releases"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    series_name = Column(String(500), nullable=True, index=True)
    volume_number = Column(String(50), nullable=True)
    isbn_13 = Column(String(13), nullable=True, unique=True, index=True)
    isbn_10 = Column(String(10), nullable=True)
    release_date = Column(Date, nullable=False, index=True)
    publisher_id = Column(Integer, ForeignKey("publishers.id"), nullable=False, index=True)
    format = Column(String(50), nullable=True)  # Paperback, Hardcover, etc.
    page_count = Column(Integer, nullable=True)
    price_usd = Column(Numeric(8, 2), nullable=True)
    price_gbp = Column(Numeric(8, 2), nullable=True)
    cover_image_url = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    demographic = Column(String(50), nullable=True)  # Shonen, Shojo, Seinen, Josei
    genres = Column(JSON, nullable=True)  # List of genres
    regions = Column(JSON, nullable=True)  # List of regions (us, uk, etc.)
    authors = Column(JSON, nullable=True)  # List of authors
    illustrators = Column(JSON, nullable=True)  # List of illustrators
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    source_metadata = Column(JSON, nullable=True)  # Additional metadata from sources

    # Relationships
    publisher = relationship("Publisher", back_populates="releases")
    source_records = relationship("SourceRecord", back_populates="manga_release", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<MangaRelease(id={self.id}, title='{self.title}', release_date={self.release_date})>"


class SourceRecord(Base):
    """Source record for tracking external data sources."""

    __tablename__ = "source_records"

    id = Column(Integer, primary_key=True, index=True)
    manga_release_id = Column(Integer, ForeignKey("manga_releases.id"), nullable=False, index=True)
    source_name = Column(String(100), nullable=False, index=True)
    external_id = Column(String(255), nullable=False)
    source_url = Column(Text, nullable=True)
    raw_data = Column(JSON, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    manga_release = relationship("MangaRelease", back_populates="source_records")

    def __repr__(self) -> str:
        return f"<SourceRecord(id={self.id}, source='{self.source_name}', external_id='{self.external_id}')>"
