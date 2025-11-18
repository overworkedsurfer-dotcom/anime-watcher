"""Database seeding utilities."""
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from app.sources.mock_source import MockSource
from app.repositories.publisher_repository import PublisherRepository
from app.repositories.release_repository import ReleaseRepository


async def seed_database(db: AsyncSession):
    """Seed database with initial data."""
    print("Seeding database...")

    # Create publishers
    publisher_repo = PublisherRepository(db)
    release_repo = ReleaseRepository(db)

    publishers = {
        "VIZ Media": await publisher_repo.get_or_create(
            name="VIZ Media",
            slug="viz-media",
            country="US",
            website_url="https://www.viz.com"
        ),
        "Kodansha Comics": await publisher_repo.get_or_create(
            name="Kodansha Comics",
            slug="kodansha-comics",
            country="US",
            website_url="https://kodansha.us"
        ),
        "Seven Seas": await publisher_repo.get_or_create(
            name="Seven Seas",
            slug="seven-seas",
            country="US",
            website_url="https://sevenseasentertainment.com"
        ),
        "Yen Press": await publisher_repo.get_or_create(
            name="Yen Press",
            slug="yen-press",
            country="US",
            website_url="https://yenpress.com"
        ),
    }

    await db.commit()
    print(f"Created {len(publishers)} publishers")

    # Generate mock releases
    mock_source = MockSource()
    today = date.today()

    # Generate releases for:
    # - Last month (to have some past data)
    # - Current month
    # - Next 3 months
    start_date = today.replace(day=1) - timedelta(days=30)
    end_date = today + timedelta(days=120)

    raw_releases = await mock_source.fetch_releases(start_date, end_date)
    print(f"Generated {len(raw_releases)} mock releases")

    # Convert to database format
    created_count = 0
    for raw_release in raw_releases:
        publisher = publishers.get(raw_release.publisher_name)
        if not publisher:
            continue

        try:
            await release_repo.create(
                title=raw_release.title,
                series_name=raw_release.series_name,
                volume_number=raw_release.volume_number,
                isbn_13=raw_release.isbn_13,
                isbn_10=raw_release.isbn_10,
                release_date=raw_release.release_date,
                publisher_id=publisher.id,
                format=raw_release.format,
                page_count=raw_release.page_count,
                price_usd=raw_release.price_usd,
                price_gbp=raw_release.price_gbp,
                cover_image_url=raw_release.cover_image_url,
                description=raw_release.description,
                demographic=raw_release.demographic,
                genres=raw_release.genres,
                regions=raw_release.regions,
                authors=raw_release.authors,
                illustrators=raw_release.illustrators,
            )
            created_count += 1
        except Exception as e:
            print(f"Error creating release: {e}")
            continue

    await db.commit()
    print(f"Created {created_count} releases")
    print("Database seeding complete!")
