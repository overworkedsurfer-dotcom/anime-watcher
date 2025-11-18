# Manga Release Radar - Technical Design Document

**Version:** 1.0
**Date:** November 2025
**Status:** Design Phase

---

## 1. Executive Summary

Manga Release Radar is a mobile-first web application that aggregates English-language manga release information from multiple sources, providing fans with a centralized, cute, and user-friendly interface to browse current and upcoming releases.

### Key Features
- Browse up to 100 latest releases from current month
- View up to 100 upcoming releases from next 3-4 months
- Multi-source data aggregation with deduplication
- Filtering by publisher, region, genre/demographic
- Full-text search by title/series
- Responsive, pastel-themed UI with shadcn/ui components

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                          │
│                                                              │
│  Next.js 14+ (App Router) + React + TypeScript              │
│  Tailwind CSS + shadcn/ui                                   │
│  Mobile-first responsive design                              │
└──────────────────────┬───────────────────────────────────────┘
                       │ HTTPS/REST
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      API GATEWAY LAYER                       │
│                                                              │
│  FastAPI (Python 3.11+)                                     │
│  - CORS middleware                                           │
│  - Rate limiting                                             │
│  - Request validation (Pydantic)                            │
│  - Error handling                                            │
└──────────────────────┬───────────────────────────────────────┘
                       │
         ┌─────────────┼─────────────┐
         │             │             │
         ▼             ▼             ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Release   │ │   Search    │ │  Metadata   │
│  Service    │ │  Service    │ │  Service    │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       └───────────────┼───────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                         │
│                                                              │
│  - SQLAlchemy (async) ORM                                   │
│  - Repository pattern                                        │
│  - Database migrations (Alembic)                            │
└──────────────────────┬──────────────────┬───────────────────┘
                       │                  │
                       ▼                  ▼
              ┌─────────────┐    ┌─────────────┐
              │ PostgreSQL  │    │    Redis    │
              │  Database   │    │   Cache     │
              └─────────────┘    └─────────────┘
                       ▲
                       │
┌─────────────────────────────────────────────────────────────┐
│                   DATA INGESTION LAYER                       │
│                                                              │
│  Background Workers (Celery/APScheduler)                    │
│  - Source managers                                           │
│  - Deduplication engine                                     │
│  - Data enrichment                                           │
└──────────────────────┬───────────────────────────────────────┘
                       │
       ┌───────────────┼───────────────┬──────────────┐
       │               │               │              │
       ▼               ▼               ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  MangaDex   │ │   Anime     │ │  Publisher  │ │   Retail    │
│   Source    │ │  Planet     │ │  Sources    │ │  Sources    │
│             │ │   Source    │ │  (Viz, etc) │ │ (Amazon,etc)│
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
```

### 2.2 Technology Stack

#### Frontend
- **Framework:** Next.js 14+ (App Router)
- **Language:** TypeScript 5+
- **UI Library:** React 18+
- **Styling:** Tailwind CSS 3+
- **Component Library:** shadcn/ui
- **State Management:** React Query (TanStack Query) for server state
- **HTTP Client:** Fetch API / Axios
- **Date Handling:** date-fns
- **Icons:** Lucide React

#### Backend
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.11+
- **ASGI Server:** Uvicorn
- **Validation:** Pydantic v2
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic
- **Background Tasks:** APScheduler (or Celery for production)
- **HTTP Client:** httpx (async)

#### Data & Infrastructure
- **Database:** PostgreSQL 15+ (SQLite for dev)
- **Cache:** Redis 7+
- **Containerization:** Docker + Docker Compose
- **Process Manager:** Supervisor (for production)

---

## 3. Database Schema

### 3.1 Entity Relationship Diagram

```
┌─────────────────────────────────────┐
│           manga_releases            │
├─────────────────────────────────────┤
│ id (PK)                INT          │
│ title                  VARCHAR(500) │
│ series_name            VARCHAR(500) │
│ volume_number          VARCHAR(50)  │
│ isbn_13                VARCHAR(13)  │
│ isbn_10                VARCHAR(10)  │
│ release_date           DATE         │
│ publisher_id (FK)      INT          │
│ format                 VARCHAR(50)  │
│ page_count             INT          │
│ price_usd              DECIMAL(8,2) │
│ price_gbp              DECIMAL(8,2) │
│ cover_image_url        TEXT         │
│ description            TEXT         │
│ demographic            VARCHAR(50)  │
│ genres                 JSONB        │
│ regions                JSONB        │
│ authors                JSONB        │
│ illustrators           JSONB        │
│ created_at             TIMESTAMP    │
│ updated_at             TIMESTAMP    │
│ source_metadata        JSONB        │
└──────────────┬──────────────────────┘
               │
               │ Many-to-One
               ▼
┌─────────────────────────────────────┐
│            publishers               │
├─────────────────────────────────────┤
│ id (PK)                INT          │
│ name                   VARCHAR(200) │
│ slug                   VARCHAR(200) │
│ country                VARCHAR(2)   │
│ website_url            TEXT         │
│ logo_url               TEXT         │
│ created_at             TIMESTAMP    │
│ updated_at             TIMESTAMP    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          source_records             │
├─────────────────────────────────────┤
│ id (PK)                INT          │
│ manga_release_id (FK)  INT          │
│ source_name            VARCHAR(100) │
│ external_id            VARCHAR(255) │
│ source_url             TEXT         │
│ raw_data               JSONB        │
│ fetched_at             TIMESTAMP    │
│ created_at             TIMESTAMP    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          data_sources               │
├─────────────────────────────────────┤
│ id (PK)                INT          │
│ name                   VARCHAR(100) │
│ slug                   VARCHAR(100) │
│ source_type            VARCHAR(50)  │
│ is_active              BOOLEAN      │
│ priority               INT          │
│ config                 JSONB        │
│ last_sync_at           TIMESTAMP    │
│ created_at             TIMESTAMP    │
│ updated_at             TIMESTAMP    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│           sync_jobs                 │
├─────────────────────────────────────┤
│ id (PK)                INT          │
│ source_id (FK)         INT          │
│ started_at             TIMESTAMP    │
│ completed_at           TIMESTAMP    │
│ status                 VARCHAR(50)  │
│ records_fetched        INT          │
│ records_created        INT          │
│ records_updated        INT          │
│ error_message          TEXT         │
│ metadata               JSONB        │
└─────────────────────────────────────┘
```

### 3.2 Indexes

```sql
-- Performance indexes
CREATE INDEX idx_releases_date ON manga_releases(release_date);
CREATE INDEX idx_releases_publisher ON manga_releases(publisher_id);
CREATE INDEX idx_releases_isbn13 ON manga_releases(isbn_13);
CREATE INDEX idx_releases_series ON manga_releases(series_name);
CREATE INDEX idx_releases_title_trgm ON manga_releases USING gin(title gin_trgm_ops);
CREATE INDEX idx_source_records_release ON source_records(manga_release_id);
CREATE INDEX idx_source_records_external ON source_records(source_name, external_id);

-- Full-text search
CREATE INDEX idx_releases_fts ON manga_releases USING gin(
  to_tsvector('english', title || ' ' || COALESCE(series_name, ''))
);
```

---

## 4. API Design

### 4.1 Base URL Structure

- **Production:** `https://api.mangareleaseradar.com/v1`
- **Development:** `http://localhost:8000/v1`

### 4.2 Core Endpoints

#### GET `/releases/current`
Get releases from the current calendar month.

**Query Parameters:**
- `limit` (int, default=100, max=100): Number of results
- `offset` (int, default=0): Pagination offset
- `publisher` (str, optional): Filter by publisher slug
- `region` (str, optional): Filter by region (us, uk, etc.)
- `format` (str, optional): Filter by format
- `sort` (str, default="date"): Sort by date, title, or publisher

**Response:**
```json
{
  "data": [
    {
      "id": 1234,
      "title": "Chainsaw Man, Vol. 15",
      "series_name": "Chainsaw Man",
      "volume_number": "15",
      "isbn_13": "9781974743192",
      "release_date": "2025-11-05",
      "publisher": {
        "id": 1,
        "name": "VIZ Media",
        "slug": "viz-media"
      },
      "format": "Paperback",
      "page_count": 192,
      "price_usd": 11.99,
      "cover_image_url": "https://...",
      "description": "...",
      "demographic": "Shonen",
      "genres": ["Action", "Horror", "Supernatural"],
      "regions": ["us", "uk"],
      "authors": ["Tatsuki Fujimoto"],
      "illustrators": ["Tatsuki Fujimoto"]
    }
  ],
  "meta": {
    "total": 87,
    "limit": 100,
    "offset": 0,
    "month": "2025-11"
  }
}
```

#### GET `/releases/upcoming`
Get releases from the next 3-4 months.

**Query Parameters:** (same as `/releases/current`)
- `months` (int, default=3, max=4): Number of months ahead

**Response:**
```json
{
  "data": {
    "2025-12": [/* releases */],
    "2026-01": [/* releases */],
    "2026-02": [/* releases */]
  },
  "meta": {
    "total": 245,
    "months_covered": ["2025-12", "2026-01", "2026-02"]
  }
}
```

#### GET `/releases/search`
Full-text search for releases.

**Query Parameters:**
- `q` (str, required): Search query
- `limit` (int, default=50, max=100)
- `offset` (int, default=0)
- `date_from` (date, optional): Filter start date
- `date_to` (date, optional): Filter end date

**Response:**
```json
{
  "data": [/* releases */],
  "meta": {
    "total": 12,
    "query": "chainsaw man"
  }
}
```

#### GET `/publishers`
Get all publishers.

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "VIZ Media",
      "slug": "viz-media",
      "country": "US",
      "release_count": 145
    }
  ]
}
```

#### GET `/metadata/filters`
Get available filter options.

**Response:**
```json
{
  "publishers": [{"id": 1, "name": "VIZ Media", "slug": "viz-media"}],
  "regions": ["us", "uk", "ca", "au"],
  "formats": ["Paperback", "Hardcover", "Digital"],
  "demographics": ["Shonen", "Shojo", "Seinen", "Josei"],
  "genres": ["Action", "Romance", "Horror", ...]
}
```

### 4.3 Error Responses

All errors follow this structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid query parameter",
    "details": {
      "field": "limit",
      "reason": "Must be between 1 and 100"
    }
  }
}
```

**Error Codes:**
- `VALIDATION_ERROR` (400)
- `NOT_FOUND` (404)
- `RATE_LIMIT_EXCEEDED` (429)
- `INTERNAL_ERROR` (500)

---

## 5. Data Source Architecture

### 5.1 Source Abstraction

```python
from typing import Protocol, List
from datetime import date
from dataclasses import dataclass

@dataclass
class RawRelease:
    """Raw release data from external source."""
    title: str
    series_name: str | None
    volume_number: str | None
    isbn_13: str | None
    isbn_10: str | None
    release_date: date
    publisher_name: str
    format: str | None
    page_count: int | None
    price_usd: float | None
    price_gbp: float | None
    cover_image_url: str | None
    description: str | None
    demographic: str | None
    genres: list[str]
    regions: list[str]
    authors: list[str]
    illustrators: list[str]
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
        region_filter: list[str] | None = None,
    ) -> list[RawRelease]:
        """Fetch releases from this source."""
        ...

    async def health_check(self) -> bool:
        """Check if source is accessible."""
        ...
```

### 5.2 Planned Data Sources

#### Priority 1 (Must-Have)
1. **MangaDex API**
   - Free, comprehensive API
   - Good coverage of English releases
   - Well-documented

2. **Anime Planet**
   - Community-driven database
   - Good metadata quality

3. **League of Comic Geeks**
   - Excellent for release dates
   - Covers many publishers

#### Priority 2 (Nice-to-Have)
4. **Publisher Direct (Web Scraping)**
   - VIZ Media
   - Kodansha
   - Seven Seas Entertainment
   - Yen Press
   - Dark Horse

5. **Retailer Calendars**
   - Amazon (via Product Advertising API if available)
   - Book Depository
   - Barnes & Noble

### 5.3 Deduplication Strategy

Releases are deduplicated using a multi-step process:

1. **Primary Key:** ISBN-13 (if available)
2. **Secondary Key:** Fuzzy match on `(series_name, volume_number, publisher)`
3. **Tertiary Key:** Fuzzy match on `title` with date proximity

```python
def calculate_similarity_score(r1: RawRelease, r2: RawRelease) -> float:
    """Calculate similarity score between two releases."""
    score = 0.0

    # ISBN match (strongest signal)
    if r1.isbn_13 and r2.isbn_13 and r1.isbn_13 == r2.isbn_13:
        return 1.0

    # Series + volume match
    if r1.series_name and r2.series_name:
        series_sim = fuzz.ratio(r1.series_name, r2.series_name) / 100
        score += series_sim * 0.4

        if r1.volume_number == r2.volume_number:
            score += 0.3

    # Title match
    title_sim = fuzz.ratio(r1.title, r2.title) / 100
    score += title_sim * 0.2

    # Publisher match
    if r1.publisher_name == r2.publisher_name:
        score += 0.1

    return score

# Threshold for deduplication: 0.85
```

### 5.4 Data Enrichment

After deduplication, releases are enriched with:
- Missing ISBNs (lookup via OpenLibrary API)
- Cover images (highest quality source preferred)
- Descriptions (longest/best description)
- Genres/demographics (merge from all sources)

---

## 6. Caching Strategy

### 6.1 Cache Layers

```
┌─────────────────────────────────────┐
│        Browser Cache (Client)       │
│  - Static assets: 1 year             │
│  - API responses: 5 minutes          │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│          CDN Cache (Edge)           │
│  - Static assets: 1 year             │
│  - API responses: 1 minute           │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│      Application Cache (Redis)      │
│  - Current month: 1 hour             │
│  - Upcoming months: 6 hours          │
│  - Search results: 30 minutes        │
│  - Metadata: 24 hours                │
└─────────────────────────────────────┘
                  ↓
┌─────────────────────────────────────┐
│          Database (Source)          │
└─────────────────────────────────────┘
```

### 6.2 Cache Invalidation

- **Time-based:** Expire after TTL
- **Event-based:** Invalidate on data sync completion
- **Manual:** Admin API endpoint for cache clearing

---

## 7. Frontend Architecture

### 7.1 Page Structure

```
/
├── app/
│   ├── layout.tsx                 # Root layout
│   ├── page.tsx                   # Home page (current month)
│   ├── upcoming/
│   │   └── page.tsx              # Upcoming releases
│   ├── search/
│   │   └── page.tsx              # Search page
│   └── api/                      # API routes (if needed)
├── components/
│   ├── ui/                       # shadcn/ui components
│   ├── layout/
│   │   ├── Header.tsx
│   │   ├── Footer.tsx
│   │   └── Navigation.tsx
│   ├── releases/
│   │   ├── ReleaseCard.tsx
│   │   ├── ReleaseGrid.tsx
│   │   ├── ReleaseList.tsx
│   │   └── MonthSection.tsx
│   └── filters/
│       ├── FilterBar.tsx
│       ├── PublisherFilter.tsx
│       ├── RegionFilter.tsx
│       └── SearchBar.tsx
├── lib/
│   ├── api/                      # API client
│   ├── hooks/                    # Custom React hooks
│   ├── utils/                    # Utility functions
│   └── types/                    # TypeScript types
└── styles/
    └── globals.css               # Global styles + Tailwind
```

### 7.2 Key Components

#### ReleaseCard
Displays individual manga release with:
- Cover image
- Title + volume
- Release date
- Publisher
- Price
- Quick actions (view details, external links)

#### FilterBar
Provides filtering UI:
- Publisher dropdown
- Region toggle
- Format selector
- Genre/demographic tags

#### MonthSection
Groups releases by month with:
- Month header
- Release count
- Grid/list view toggle

### 7.3 Design System (Pastel Theme)

```typescript
// tailwind.config.ts theme extension
export const theme = {
  colors: {
    primary: {
      50: '#fef5ff',
      100: '#fde8ff',
      200: '#fbd5ff',
      300: '#f8b4fe',
      400: '#f384fb',
      500: '#e750f4',
      600: '#c729d6',
      700: '#a11cb3',
      800: '#841a92',
      900: '#6e1a76',
    },
    pastel: {
      pink: '#ffc4dd',
      purple: '#d4a5ff',
      blue: '#a8d8ff',
      green: '#b8f0d0',
      yellow: '#fff3b8',
      orange: '#ffd4a3',
    },
    neutral: {
      // Warm grays
    }
  },
  borderRadius: {
    'xl': '1rem',
    '2xl': '1.5rem',
    '3xl': '2rem',
  }
}
```

**Visual Design Principles:**
- Rounded corners everywhere (minimum 0.75rem)
- Soft shadows for depth
- Pastel color palette with high contrast text
- Generous spacing (minimum 1rem between sections)
- Playful hover animations (scale, color shift)
- Smooth transitions (200-300ms)

---

## 8. Deployment Architecture

### 8.1 Docker Setup

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      - backend

  db:
    image: postgres:15-alpine
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=manga_radar
      - POSTGRES_USER=manga_user
      - POSTGRES_PASSWORD=${DB_PASSWORD}

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

  worker:
    build: ./backend
    command: python -m app.worker
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

volumes:
  postgres_data:
  redis_data:
```

### 8.2 Production Deployment (Render/Railway)

**Backend Service:**
- Type: Web Service
- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `/health`

**Frontend Service:**
- Type: Static Site / Web Service
- Build: `npm run build`
- Start: `npm start`

**Database:**
- Managed PostgreSQL instance
- Regular backups enabled

**Redis:**
- Managed Redis instance
- Persistence enabled

**Background Worker:**
- Type: Background Worker
- Start: `python -m app.worker`

---

## 9. Data Sync Strategy

### 9.1 Sync Schedule

```python
# Sync jobs scheduled via APScheduler
schedules = {
    "current_month": "0 */6 * * *",    # Every 6 hours
    "upcoming_months": "0 2 * * *",     # Daily at 2 AM
    "metadata_refresh": "0 4 * * 0",    # Weekly on Sunday at 4 AM
}
```

### 9.2 Sync Process

```python
async def sync_releases(
    source: MangaSource,
    start_date: date,
    end_date: date
) -> SyncResult:
    """Sync releases from a source."""

    # 1. Fetch raw data
    raw_releases = await source.fetch_releases(start_date, end_date)

    # 2. Deduplicate with existing data
    deduplicated = await deduplication_engine.process(raw_releases)

    # 3. Enrich with additional data
    enriched = await enrichment_service.enrich(deduplicated)

    # 4. Persist to database
    saved = await release_repository.bulk_upsert(enriched)

    # 5. Invalidate cache
    await cache.invalidate_pattern("releases:*")

    return SyncResult(
        fetched=len(raw_releases),
        created=saved.created,
        updated=saved.updated
    )
```

---

## 10. Performance Targets

### 10.1 API Performance
- **Response time:** P95 < 200ms, P99 < 500ms
- **Throughput:** 100 req/s per instance
- **Database queries:** < 50ms for indexed queries

### 10.2 Frontend Performance
- **First Contentful Paint:** < 1.5s
- **Largest Contentful Paint:** < 2.5s
- **Time to Interactive:** < 3.5s
- **Lighthouse Score:** > 90 (all categories)

### 10.3 Data Freshness
- **Current month:** Max 6 hours lag
- **Upcoming months:** Max 24 hours lag
- **Search index:** Real-time updates

---

## 11. Security Considerations

### 11.1 API Security
- Rate limiting: 100 requests per minute per IP
- CORS: Whitelist frontend domain only
- Input validation: Pydantic models
- SQL injection: Parameterized queries via ORM
- XSS prevention: Output encoding

### 11.2 Data Privacy
- No user data collection (v1)
- Anonymous usage analytics only
- GDPR-compliant (no personal data)

---

## 12. Monitoring & Observability

### 12.1 Metrics to Track
- API response times (per endpoint)
- Database query performance
- Cache hit rates
- Sync job success/failure rates
- Error rates by type

### 12.2 Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Correlation IDs for request tracing

### 12.3 Alerts
- API error rate > 5%
- Database connection failures
- Sync job failures
- Redis unavailability

---

## 13. Testing Strategy

### 13.1 Backend Testing
- **Unit tests:** 80%+ coverage
  - Business logic
  - Data models
  - Utilities
- **Integration tests:**
  - API endpoints
  - Database operations
  - External source clients
- **E2E tests:**
  - Critical user flows

### 13.2 Frontend Testing
- **Unit tests:** Component logic
- **Integration tests:** Page flows
- **Visual regression:** Chromatic/Percy
- **E2E tests:** Playwright

---

## 14. Future Enhancements (Post-v1)

1. **User Accounts**
   - Watchlists
   - Email notifications
   - Personalized recommendations

2. **Advanced Features**
   - Price tracking & alerts
   - Series tracking (follow a series)
   - Reading lists
   - Publisher news integration

3. **Admin Dashboard**
   - Manual data correction
   - Source management UI
   - Analytics dashboard

4. **Mobile Apps**
   - React Native / Flutter
   - Push notifications

5. **API for Third Parties**
   - Public API with authentication
   - Webhooks for release notifications

---

## 15. Success Metrics

### 15.1 Technical Metrics
- 99.5% uptime
- < 1% error rate
- < 500ms P95 response time
- 80%+ cache hit rate

### 15.2 Product Metrics
- Monthly active users
- Releases displayed vs. actual market coverage
- Search success rate
- User engagement (time on site, pages per session)

---

## Appendix A: File Structure

```
manga-release-radar/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── releases.py
│   │   │   │   ├── publishers.py
│   │   │   │   └── metadata.py
│   │   │   └── deps.py
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── release.py
│   │   │   ├── publisher.py
│   │   │   └── source.py
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── release.py
│   │   │   └── common.py
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── release_service.py
│   │   │   ├── search_service.py
│   │   │   └── cache_service.py
│   │   ├── repositories/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   └── release_repository.py
│   │   ├── sources/
│   │   │   ├── __init__.py
│   │   │   ├── base.py
│   │   │   ├── mangadex.py
│   │   │   ├── anime_planet.py
│   │   │   └── league_of_comic_geeks.py
│   │   ├── workers/
│   │   │   ├── __init__.py
│   │   │   ├── scheduler.py
│   │   │   └── sync_tasks.py
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── deduplication.py
│   │       └── enrichment.py
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── styles/
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── next.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Appendix B: Example API Responses

See Section 4.2 for detailed examples.

---

## Appendix C: Third-Party APIs & Resources

### APIs
- **MangaDex:** https://api.mangadex.org/docs/
- **Anime Planet:** Community API (scraping may be needed)
- **League of Comic Geeks:** https://leagueofcomicgeeks.com/

### Libraries
- **Python:** httpx, beautifulsoup4, fuzzywuzzy, python-dateutil
- **TypeScript:** date-fns, fuse.js, react-query

---

**End of Technical Design Document**
