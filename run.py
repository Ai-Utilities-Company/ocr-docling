#!/usr/bin/env python3
"""
Script to run OCR Docling API application with Docker
Works on Windows, Linux and macOS
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path


def check_command(command: str) -> bool:
    """Checks if command is available"""
    try:
        subprocess.run([command, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def run_command(command: list, check: bool = True) -> subprocess.CompletedProcess:
    """Runs command and returns result"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(command)}")
        print(f"   {e.stderr}")
        return e


def check_health(url: str, timeout: int = 10) -> bool:
    """Checks if application responds"""
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


def main():
    """Main script function"""
    print("🚀 Starting OCR Docling API...")

    # Check if Docker is installed
    if not check_command("docker"):
        print("❌ Docker is not installed. Install Docker and try again.")
        sys.exit(1)

    # Check if docker-compose is installed
    if not check_command("docker-compose"):
        print(
            "❌ docker-compose is not installed. Install docker-compose and try again."
        )
        sys.exit(1)

    # Set environment (can be overridden by ENVIRONMENT variable)
    environment = os.getenv("ENVIRONMENT", "development")
    port = os.getenv("PORT", "8000")
    debug = os.getenv("DEBUG", "false").lower() == "true"

    # Display configuration
    print("📋 Configuration:")
    print(f"   Environment: {environment}")
    print(f"   Port: {port}")
    print(f"   Debug: {debug}")

    # Set environment variables for docker-compose
    env = os.environ.copy()
    env["ENVIRONMENT"] = environment
    if port != "8000":
        env["PORT"] = port
    if debug:
        env["DEBUG"] = "true"

    # Build and run containers
    print("📦 Building and starting containers...")
    result = run_command(["docker-compose", "up", "--build", "-d"], check=False)

    if result.returncode != 0:
        print("❌ Error starting containers:")
        print(result.stderr)
        sys.exit(1)

    # Check status
    print("⏳ Checking application status...")
    time.sleep(5)

    # Check if application responds
    health_url = f"http://localhost:{port}/health"
    if check_health(health_url):
        print("✅ OCR Docling API is running!")
        print(f"   Available at: http://localhost:{port}")
        print(f" API Documentation: http://localhost:{port}/docs")
        print(f"   Health check: http://localhost:{port}/health")
        print()
        print("To stop application, run: docker-compose down")
        print("To see logs: docker-compose logs -f")
        print()
        print("💡 Tips:")
        print("   - Change environment: ENVIRONMENT=staging python run.py")
        print("   - Change port: PORT=9000 python run.py")
        print("   - Enable debug: DEBUG=true python run.py")
    else:
        print("❌ Application is not responding. Check logs: docker-compose logs")


if __name__ == "__main__":
    main()
