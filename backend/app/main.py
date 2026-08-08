from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import logger
from app.core.ai_tracker import ai_tracker
from app.database.session import init_db
from app.services.scheduler_service import scheduler_service
from app.routers import (
    agent_router,
    feed_router,
    topics_router,
    editorial_router,
    rejected_router,
    sources_router,
    memory_router,
    analytics_router,
    ai_usage_router
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing AutoPersona AI backend...")
    init_db()
    
    # Start autonomous background scheduler
    scheduler_service.start()

    ai_tracker.log_event(
        milestone="Prompt 9: API",
        prompt_title="Application Lifespan Startup",
        prompt_text="Initializing database, routers, and APScheduler background tasks.",
        output_summary="All 9 API modules active and scheduler running.",
        model="gpt-4o-mini"
    )
    yield
    logger.info("Shutting down AutoPersona AI backend...")
    scheduler_service.shutdown()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Production-ready Autonomous AI Persona Platform (Ada - AI Security)",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register All API Routers
app.include_router(agent_router)
app.include_router(feed_router)
app.include_router(topics_router)
app.include_router(editorial_router)
app.include_router(rejected_router)
app.include_router(sources_router)
app.include_router(memory_router)
app.include_router(analytics_router)
app.include_router(ai_usage_router)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "environment": settings.APP_ENV
    }

@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to AutoPersona AI Platform API",
        "docs_url": "/docs",
        "persona": {
            "name": settings.PERSONA_NAME,
            "domain": settings.PERSONA_DOMAIN
        }
    }
