"""Mock data source for testing and initial data."""
from datetime import date, timedelta
from typing import List, Optional
import random

from app.sources.base import RawRelease


class MockSource:
    """Mock source that generates sample manga releases."""

    name = "mock"
    priority = 999  # Low priority

    # Sample data
    SERIES = [
        ("Chainsaw Man", "Shonen", ["Action", "Horror", "Supernatural"], "VIZ Media"),
        ("My Hero Academia", "Shonen", ["Action", "Superhero"], "VIZ Media"),
        ("Spy x Family", "Shonen", ["Action", "Comedy"], "VIZ Media"),
        ("Witch Hat Atelier", "Shonen", ["Fantasy", "Adventure"], "Kodansha Comics"),
        ("Blue Period", "Seinen", ["Drama", "Slice of Life"], "Kodansha Comics"),
        ("Skip and Loafer", "Shojo", ["Romance", "Comedy"], "Seven Seas"),
        ("Shadows House", "Shonen", ["Mystery", "Supernatural"], "Yen Press"),
        ("Vinland Saga", "Seinen", ["Historical", "Action"], "Kodansha Comics"),
        ("A Sign of Affection", "Josei", ["Romance", "Drama"], "Kodansha Comics"),
        ("Yotsuba&!", "Shonen", ["Slice of Life", "Comedy"], "Yen Press"),
    ]

    PUBLISHERS = {
        "VIZ Media": "viz-media",
        "Kodansha Comics": "kodansha-comics",
        "Seven Seas": "seven-seas",
        "Yen Press": "yen-press",
    }

    async def fetch_releases(
        self,
        start_date: date,
        end_date: date,
        *,
        language_filter: str = "en",
        region_filter: Optional[List[str]] = None,
    ) -> List[RawRelease]:
        """Generate mock releases."""
        releases = []
        current_date = start_date

        # Generate releases across the date range
        while current_date <= end_date:
            # Generate 2-4 releases per week
            if current_date.weekday() == 1:  # Tuesday releases
                num_releases = random.randint(2, 4)
                for _ in range(num_releases):
                    series_name, demo, genres, publisher = random.choice(self.SERIES)
                    vol_num = random.randint(1, 25)

                    release = RawRelease(
                        title=f"{series_name}, Vol. {vol_num}",
                        series_name=series_name,
                        volume_number=str(vol_num),
                        isbn_13=self._generate_isbn(),
                        isbn_10=None,
                        release_date=current_date,
                        publisher_name=publisher,
                        format=random.choice(["Paperback", "Hardcover"]),
                        page_count=random.randint(160, 240),
                        price_usd=round(random.uniform(9.99, 16.99), 2),
                        price_gbp=round(random.uniform(7.99, 13.99), 2),
                        cover_image_url=f"https://via.placeholder.com/400x600/FFE5EC/333333?text={series_name.replace(' ', '+')}+Vol.{vol_num}",
                        description=f"Volume {vol_num} of the popular {demo.lower()} manga series {series_name}.",
                        demographic=demo,
                        genres=genres,
                        regions=["us", "uk", "ca"],
                        authors=[f"Author {random.randint(1, 100)}"],
                        illustrators=[f"Illustrator {random.randint(1, 100)}"],
                        external_id=f"mock-{series_name.lower().replace(' ', '-')}-{vol_num}",
                        source_url=f"https://example.com/manga/{series_name.lower().replace(' ', '-')}/vol-{vol_num}",
                        raw_data={},
                    )
                    releases.append(release)

            current_date += timedelta(days=1)

        return releases

    async def health_check(self) -> bool:
        """Always healthy."""
        return True

    def _generate_isbn(self) -> str:
        """Generate a fake ISBN-13."""
        # ISBN-13 format: 978-1-234567-89-0
        prefix = "978"
        group = "1"
        publisher = str(random.randint(100000, 999999))
        title = str(random.randint(10, 99))

        # Calculate check digit (simplified)
        digits = prefix + group + publisher + title
        check_digit = str((10 - sum((3 if i % 2 else 1) * int(d) for i, d in enumerate(digits))) % 10)

        return prefix + group + publisher + title + check_digit
