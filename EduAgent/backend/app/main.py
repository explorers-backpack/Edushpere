"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db, close_db
from app.core.redis import close_redis

from app.api.user.router import router as user_router
from app.api.profile_agent.router import router as profile_router
from app.api.path_agent.router import router as path_router
from app.api.resource_agent.router import router as resource_router
from app.api.evaluate_agent.router import router as evaluate_router
from app.api.tutor_agent.router import router as tutor_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()
    await close_redis()


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    app = FastAPI(
        title="EduAgent API",
        description="Personalized Learning Resource Generation and Multi-Agent Learning System",
        version="1.0.0",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(user_router)
    app.include_router(profile_router)
    app.include_router(path_router)
    app.include_router(resource_router)
    app.include_router(evaluate_router)
    app.include_router(tutor_router)

    @app.get("/")
    async def root():
        """Health check endpoint."""
        return {"status": "healthy", "app": "EduAgent"}

    @app.get("/health")
    async def health():
        """Detailed health check."""
        return {
            "status": "healthy",
            "environment": settings.APP_ENV,
            "debug": settings.DEBUG,
        }

    return app


app = create_app()
