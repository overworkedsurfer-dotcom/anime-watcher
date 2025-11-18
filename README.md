# 📚 Manga Release Radar

> A cute, mobile-first web app for tracking English manga releases

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 14](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)

## ✨ Features

- **📅 Current Month Releases:** Browse up to 100 latest English manga releases from the current month
- **🔮 Upcoming Releases:** See what's coming in the next 3-4 months
- **🔍 Smart Search:** Full-text search with fuzzy matching
- **🎯 Advanced Filtering:** Filter by publisher, region, format, genre, and demographic
- **🎨 Cute Pastel UI:** Mobile-first responsive design with playful animations
- **🔄 Multi-Source Aggregation:** Data from MangaDex, Anime Planet, League of Comic Geeks, and more
- **⚡ Fast & Cached:** Redis caching for lightning-fast responses
- **🌙 Dark Mode:** Easy on the eyes (optional feature)

## 🏗️ Architecture

**Frontend:**
- Next.js 14 (App Router) + React 18
- TypeScript 5 with strict mode
- Tailwind CSS 3 + shadcn/ui components
- React Query for server state management

**Backend:**
- FastAPI with Python 3.11+
- PostgreSQL 15 database
- Redis 7 for caching
- Async I/O throughout
- SQLAlchemy 2.0 (async ORM)

**Infrastructure:**
- Docker & Docker Compose
- Background workers (APScheduler)
- Multi-source data aggregation
- Automated deduplication engine

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/manga-release-radar.git
cd manga-release-radar

# Copy environment files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# Start all services
docker-compose up --build

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database
alembic upgrade head

# Seed initial data (optional)
python -m app.cli seed

# Run development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Access at http://localhost:3000
```

## 📖 Documentation

- **[Technical Design Document](./TECHNICAL_DESIGN.md):** Comprehensive technical specification
- **[Implementation Plan](./IMPLEMENTATION_PLAN.md):** Phase-by-phase development roadmap
- **[API Documentation](http://localhost:8000/docs):** Interactive OpenAPI docs (when running)

## 🗂️ Project Structure

```
manga-release-radar/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   ├── repositories/   # Data access layer
│   │   ├── sources/        # External data sources
│   │   ├── workers/        # Background tasks
│   │   └── utils/          # Utilities
│   ├── alembic/            # Database migrations
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # Next.js frontend
│   ├── app/               # App Router pages
│   ├── components/        # React components
│   ├── lib/              # Utilities & API client
│   └── styles/           # Global styles
├── docker-compose.yml     # Docker orchestration
└── README.md             # This file
```

## 🎨 Design Philosophy

Manga Release Radar embraces a **cute, cozy, and approachable** design language:

- **Pastel Color Palette:** Soft pinks, purples, blues, and greens
- **Rounded Corners:** Everything has generous border-radius (minimum 0.75rem)
- **Playful Animations:** Hover effects, smooth transitions, micro-interactions
- **Mobile-First:** Designed for phones, scales beautifully to desktop
- **Accessibility:** WCAG 2.1 AA compliant, keyboard navigable

## 🔌 API Endpoints

### Core Endpoints

- `GET /api/v1/releases/current` - Current month releases
- `GET /api/v1/releases/upcoming` - Upcoming releases (3-4 months)
- `GET /api/v1/releases/search` - Search releases
- `GET /api/v1/publishers` - List all publishers
- `GET /api/v1/metadata/filters` - Available filter options

### Example Request

```bash
curl "http://localhost:8000/api/v1/releases/current?publisher=viz-media&region=us&limit=10"
```

### Example Response

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
      "price_usd": 11.99,
      "cover_image_url": "https://...",
      "genres": ["Action", "Horror", "Supernatural"],
      "regions": ["us", "uk"]
    }
  ],
  "meta": {
    "total": 87,
    "limit": 10,
    "offset": 0
  }
}
```

## 🔄 Data Sources

The app aggregates data from multiple sources:

1. **MangaDex** - Comprehensive manga database with API
2. **Anime Planet** - Community-driven metadata
3. **League of Comic Geeks** - Release calendar tracking
4. **Publisher Websites** - Direct from VIZ, Kodansha, Seven Seas, etc.
5. **Retail Calendars** - Amazon, Book Depository, Barnes & Noble

All sources are deduplicated using ISBN matching and fuzzy logic.

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest                           # Run all tests
pytest --cov                     # With coverage
pytest tests/unit               # Unit tests only
pytest tests/integration        # Integration tests only
```

### Frontend Tests

```bash
cd frontend
npm test                        # Run all tests
npm run test:watch             # Watch mode
npm run test:e2e               # E2E tests (Playwright)
```

## 🚢 Deployment

### Render / Railway / Fly.io

1. **Backend Service:**
   - Build: `pip install -r backend/requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health check: `/health`

2. **Frontend Service:**
   - Build: `cd frontend && npm run build`
   - Start: `npm start`

3. **Database:** Managed PostgreSQL instance
4. **Redis:** Managed Redis instance
5. **Worker:** Background service running `python -m app.worker`

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for detailed deployment instructions.

## 🛠️ Development

### Environment Variables

#### Backend (.env)

```env
# Database
DATABASE_URL=postgresql://user:pass@localhost:5432/manga_radar

# Redis
REDIS_URL=redis://localhost:6379

# API
API_V1_PREFIX=/api/v1
CORS_ORIGINS=http://localhost:3000

# External APIs
MANGADEX_API_URL=https://api.mangadex.org
```

#### Frontend (.env.local)

```env
# API
NEXT_PUBLIC_API_URL=http://localhost:8000

# Analytics (optional)
NEXT_PUBLIC_GA_ID=your-ga-id
```

### Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "Add new field"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Code Quality

```bash
# Backend
cd backend
black .                 # Format code
ruff .                  # Lint
mypy app/              # Type check

# Frontend
cd frontend
npm run lint           # ESLint
npm run format         # Prettier
npm run type-check     # TypeScript
```

## 📊 Performance Targets

- **API Response Time:** P95 < 200ms, P99 < 500ms
- **Frontend FCP:** < 1.5s
- **Frontend LCP:** < 2.5s
- **Lighthouse Score:** > 90 (all categories)
- **Database Queries:** < 50ms for indexed queries
- **Cache Hit Rate:** > 80%
- **Uptime:** 99.5%

## 🗺️ Roadmap

### Phase 1: MVP (Current)
- ✅ Current month releases
- ✅ Upcoming releases (3-4 months)
- ✅ Search and filtering
- ✅ Multi-source aggregation
- ✅ Responsive UI with pastel theme

### Phase 2: Enhancements
- [ ] User accounts & authentication
- [ ] Watchlists & notifications
- [ ] Email alerts for new releases
- [ ] Series tracking
- [ ] Price tracking

### Phase 3: Advanced Features
- [ ] Personalized recommendations
- [ ] Reading lists
- [ ] Publisher news integration
- [ ] Mobile apps (React Native)
- [ ] Public API for third parties

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest` for backend, `npm test` for frontend)
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
6. Push to your fork
7. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Data Sources:** MangaDex, Anime Planet, League of Comic Geeks
- **UI Components:** shadcn/ui
- **Icons:** Lucide React
- **Hosting:** Render / Railway / Fly.io

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/yourusername/manga-release-radar/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/manga-release-radar/discussions)
- **Email:** support@mangareleaseradar.com

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ by manga fans, for manga fans**
