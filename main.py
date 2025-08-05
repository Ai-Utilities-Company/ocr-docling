"""Main entry point for OCR Docling API application"""

import uvicorn
from app.config import config_manager

if __name__ == "__main__":
    config = config_manager.config
    uvicorn.run(
        "app.main:app",
        host=config.server.host,
        port=config.server.port,
        reload=config.server.reload,
        log_level=config.server.log_level.lower(),
    )
