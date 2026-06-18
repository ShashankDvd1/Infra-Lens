"""
LandScope AI — FastAPI Application Entry Point.
"""

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import get_settings
from app.db.session import engine, Base
from app.api.v1 import projects, areas, search, ai, map as map_router, auth, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown events."""
    # Startup
    settings = get_settings()
    print(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"🤖 LLM: {settings.LLM_MODEL} via Groq")
    print(f"📊 Embeddings: {settings.EMBEDDING_MODEL}")
    yield
    # Shutdown
    print("👋 Shutting down LandScope AI")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="AI-powered Property Intelligence Platform",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # API routes
    app.include_router(
        projects.router,
        prefix=f"{settings.API_V1_PREFIX}/projects",
        tags=["Projects"],
    )
    app.include_router(
        areas.router,
        prefix=f"{settings.API_V1_PREFIX}/areas",
        tags=["Areas"],
    )
    app.include_router(
        search.router,
        prefix=f"{settings.API_V1_PREFIX}/search",
        tags=["Search"],
    )
    app.include_router(
        ai.router,
        prefix=f"{settings.API_V1_PREFIX}/ai",
        tags=["AI"],
    )
    app.include_router(
        map_router.router,
        prefix=f"{settings.API_V1_PREFIX}/map",
        tags=["Map"],
    )
    app.include_router(
        auth.router,
        prefix=f"{settings.API_V1_PREFIX}/auth",
        tags=["Auth"],
    )
    app.include_router(
        users.router,
        prefix=f"{settings.API_V1_PREFIX}/users",
        tags=["Users"],
    )
    
    from app.api.v1 import alerts, distress
    app.include_router(
        alerts.router,
        prefix=f"{settings.API_V1_PREFIX}/alerts",
        tags=["Alerts"],
    )
    app.include_router(
        distress.router,
        prefix=f"{settings.API_V1_PREFIX}/distress",
        tags=["Distress"],
    )

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "healthy", "app": settings.APP_NAME, "version": settings.APP_VERSION}

    # Prometheus Instrumentation
    Instrumentator().instrument(app).expose(app)

    return app


app = create_app()
