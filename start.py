#!/usr/bin/env python3
"""
Script to run OCR Docling API application directly with Python
Works on Windows, Linux and macOS
"""

import os
import sys
import uvicorn
from app.config import config_manager


def main():
    """Main script function"""
    print("🚀 Starting OCR Docling API (Python)...")

    # Get configuration
    config = config_manager.config

    # Display configuration
    print("📋 Configuration:")
    print(f"   Environment: {config.environment.value}")
    print(f"   Host: {config.server.host}")
    print(f"   Port: {config.server.port}")
    print(f"   Debug: {config.server.debug}")
    print(f"   Log Level: {config.server.log_level}")
    print(f"   CORS Origins: {', '.join(config.cors.origins)}")

    # Start application
    print(" Starting server...")
    try:
        uvicorn.run(
            "app.main:app",
            host=config.server.host,
            port=config.server.port,
            reload=config.server.reload,
            log_level=config.server.log_level.lower(),
        )
    except KeyboardInterrupt:
        print("\n👋 Stopping application...")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
