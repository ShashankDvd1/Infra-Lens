# LandScope AI

> AI-powered Property Intelligence Platform — Know where the city is growing, before prices move.

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/org/landscape-ai.git
cd landscape-ai

# 2. Copy environment file
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 3. Start all services
docker-compose up -d

# 4. Run database migrations
docker exec backend alembic upgrade head

# 5. Seed initial data
docker exec backend python -m app.db.seed

# 6. Generate embeddings for seed data
docker exec backend python -m app.rag.embeddings --generate-all

# 7. Generate AI summaries for all projects
docker exec backend python -m app.agents.intelligence_agent --summarise-all

# 8. Verify
curl http://localhost/api/v1/projects  # Should return project list
open http://localhost                   # Should show landing page
```

## Architecture

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14 (App Router) + Tailwind CSS |
| Map | Leaflet + OpenStreetMap |
| Backend | FastAPI (Python 3.11+) |
| Database | PostgreSQL 16 + PostGIS + pgvector |
| Cache | Redis |
| Object Store | MinIO |
| LLM | Llama 3.3 70B via Groq API |
| Embeddings | bge-base-en-v1.5 (sentence-transformers) |
| AI Framework | LangChain + LangGraph |

## Project Structure

```
landscape-ai/
├── frontend/          # Next.js 14 application
├── backend/           # FastAPI application
├── docker/            # Docker configurations
│   ├── nginx/         # Nginx reverse proxy config
│   ├── postgres/      # PostgreSQL init scripts
│   └── redis/         # Redis config
├── docs/              # Project documentation
├── docker-compose.yml
├── .env.example
└── README.md
```

## Documentation

- [Problem Statement](docs/problemstatement.md)
- [Product Requirements](docs/PRD.md)
- [System Architecture](docs/architecture.md)
- [Implementation Plan](docs/implementationplan.md)
- [Edge Cases](docs/edgecase.md)

## License

MIT
