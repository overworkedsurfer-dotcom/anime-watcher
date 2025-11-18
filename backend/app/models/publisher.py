"""Publisher model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.utils.database import Base


class Publisher(Base):
    """Publisher model."""

    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True)
    slug = Column(String(200), nullable=False, unique=True, index=True)
    country = Column(String(2), nullable=True)  # ISO country code
    website_url = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    releases = relationship("MangaRelease", back_populates="publisher")

    def __repr__(self) -> str:
        return f"<Publisher(id={self.id}, name='{self.name}')>"
