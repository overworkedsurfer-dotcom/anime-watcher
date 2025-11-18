# Manga Release Radar - Quick Start Guide

Get the Manga Release Radar app running in under 5 minutes with Docker Compose!

## Prerequisites

- **Docker** and **Docker Compose** installed on your machine
- **Git** (to clone the repository)

That's it! Docker will handle all the dependencies.

## Quick Start

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd anime-watcher
```

### 2. Build and Start All Services

```bash
docker-compose up --build
```

This single command will:
- Build the backend (FastAPI) and frontend (Next.js) containers
- Start PostgreSQL database
- Start Redis cache
- Initialize the database with sample data
- Start all services

### 3. Access the Application

Once all services are running (look for "Starting server..." in the logs), open your browser:

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

## What You'll See

The application will be pre-populated with sample manga releases:

- **Current Month Releases:** Browse this month's English manga releases
- **Upcoming Releases:** See what's coming in the next 3 months
- **Search:** Search for manga by title, series, or publisher

## Stopping the Application

Press `Ctrl+C` in the terminal, then run:

```bash
docker-compose down
```

To remove all data (database, cache):

```bash
docker-compose down -v
```

## Troubleshooting

### Port Already in Use

If you see errors about ports 3000, 8000, 5432, or 6379 being in use, you can either:

1. Stop the service using that port
2. Or modify `docker-compose.yml` to use different ports

### Backend Not Starting

If the backend fails to start, check the logs:

```bash
docker-compose logs backend
```

Common issues:
- Database not ready: Wait a few seconds and restart
- Port conflicts: See "Port Already in Use" above

### Frontend Not Loading

Check frontend logs:

```bash
docker-compose logs frontend
```

The frontend might take 1-2 minutes to build on first run.

### Database Connection Errors

Make sure all services are healthy:

```bash
docker-compose ps
```

All services should show "healthy" status.

## Development Mode

The docker-compose setup is configured for development:

- **Hot reload:** Changes to code are automatically reflected
- **Database persistence:** Data is saved in Docker volumes
- **Debug mode:** Detailed error messages and logging

### Making Code Changes

1. Edit files in `backend/` or `frontend/` directories
2. Changes are automatically detected and reloaded
3. No need to restart containers (except for dependency changes)

### Viewing Logs

All services:
```bash
docker-compose logs -f
```

Specific service:
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db
```

## Next Steps

Once you have the app running:

1. **Explore the API:** Visit http://localhost:8000/docs for interactive API documentation
2. **Customize the data:** Edit `backend/app/sources/mock_source.py` to change sample data
3. **Add real data sources:** Implement MangaDex or other API integrations
4. **Customize the UI:** Modify components in `frontend/components/`

## Production Deployment

For production deployment, see [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) section on deployment.

## Need Help?

- Check the [README.md](./README.md) for detailed documentation
- Review [TECHNICAL_DESIGN.md](./TECHNICAL_DESIGN.md) for architecture details
- See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for development phases

---

**Happy Manga Tracking! 📚**
