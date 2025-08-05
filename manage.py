#!/usr/bin/env python3
"""
Script to manage OCR Docling API application
Works on Windows, Linux and macOS
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(command: list, check: bool = True) -> subprocess.CompletedProcess:
    """Runs command and returns result"""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=check)
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running command: {' '.join(command)}")
        print(f"   {e.stderr}")
        return e


def check_docker():
    """Checks if Docker is available"""
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def start_docker(
    environment: str = "development", port: str = "8000", debug: str = "false"
):
    """Starts application in Docker"""
    print("🚀 Starting OCR Docling API in Docker...")

    if not check_docker():
        print("❌ Docker is not installed.")
        return False

    env = os.environ.copy()
    env["ENVIRONMENT"] = environment
    env["PORT"] = port
    env["DEBUG"] = debug

    result = run_command(["docker-compose", "up", "--build", "-d"], check=False)
    return result.returncode == 0


def stop_docker():
    """Stops application in Docker"""
    print("🛑 Stopping application...")
    result = run_command(["docker-compose", "down"], check=False)
    return result.returncode == 0


def logs_docker():
    """Shows application logs"""
    print("📋 Application logs:")
    result = run_command(["docker-compose", "logs", "-f"], check=False)
    return result.returncode == 0


def start_python(
    environment: str = "development", port: str = "8000", debug: str = "false"
):
    """Starts application directly with Python"""
    print("🚀 Starting OCR Docling API in Python...")

    env = os.environ.copy()
    env["ENVIRONMENT"] = environment
    env["PORT"] = port
    env["DEBUG"] = debug

    try:
        subprocess.run([sys.executable, "start.py"], env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting application: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Stopping application...")
        return True


def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Manage OCR Docling API application")
    parser.add_argument(
        "command",
        choices=["start", "stop", "logs", "start-python"],
        help="Command to execute",
    )
    parser.add_argument(
        "--env",
        default="development",
        choices=["development", "staging", "production"],
        help="Environment (default: development)",
    )
    parser.add_argument("--port", default="8000", help="Port (default: 8000)")
    parser.add_argument(
        "--debug",
        default="false",
        choices=["true", "false"],
        help="Debug mode (default: false)",
    )

    args = parser.parse_args()

    if args.command == "start":
        success = start_docker(args.env, args.port, args.debug)
        if success:
            print("✅ Application started successfully!")
        else:
            print("❌ Error starting application.")
            sys.exit(1)

    elif args.command == "stop":
        success = stop_docker()
        if success:
            print("✅ Application stopped successfully!")
        else:
            print("❌ Error stopping application.")
            sys.exit(1)

    elif args.command == "logs":
        logs_docker()

    elif args.command == "start-python":
        start_python(args.env, args.port, args.debug)


if __name__ == "__main__":
    main()
