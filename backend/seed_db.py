"""Seed database script."""
import asyncio
from app.utils.database import AsyncSessionLocal, init_db
from app.utils.seed import seed_database


async def main():
    """Main function."""
    # Initialize database
    await init_db()

    # Seed data
    async with AsyncSessionLocal() as db:
        await seed_database(db)


if __name__ == "__main__":
    asyncio.run(main())
