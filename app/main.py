"""Main FastAPI application with separated logic"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.config import config_manager
from app.api import ocr, health, file_jobs


def create_app() -> FastAPI:
    """Creates FastAPI application instance"""
    config = config_manager.config

    app = FastAPI(
        title=config.api.title,
        description=config.api.description,
        version=config.api.version,
        debug=config.server.debug,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register routers
    app.include_router(health.router)
    app.include_router(ocr.router)
    app.include_router(file_jobs.router)

    return app


# Create application
app = create_app()


if __name__ == "__main__":
    config = config_manager.config
    uvicorn.run(
        "app.main:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload,
        log_level=config.server.log_level.lower(),
    )
