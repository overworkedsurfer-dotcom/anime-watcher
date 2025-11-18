"""Base repository with common CRUD operations."""
from typing import Generic, TypeVar, Type, Optional, List, Any

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Base repository with common database operations."""

    def __init__(self, model: Type[ModelType], db: AsyncSession):
        """Initialize repository."""
        self.model = model
        self.db = db

    async def get(self, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        result = await self.db.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_multi(
        self, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        result = await self.db.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(self, **kwargs: Any) -> ModelType:
        """Create a new record."""
        db_obj = self.model(**kwargs)
        self.db.add(db_obj)
        await self.db.flush()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, **kwargs: Any) -> Optional[ModelType]:
        """Update a record."""
        await self.db.execute(
            update(self.model).where(self.model.id == id).values(**kwargs)
        )
        await self.db.flush()
        return await self.get(id)

    async def delete(self, id: int) -> bool:
        """Delete a record."""
        result = await self.db.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.db.flush()
        return result.rowcount > 0

    async def count(self) -> int:
        """Count total records."""
        from sqlalchemy import func
        result = await self.db.execute(
            select(func.count()).select_from(self.model)
        )
        return result.scalar_one()
