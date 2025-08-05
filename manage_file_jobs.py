#!/usr/bin/env python3
"""
Script to manage file jobs processing
Works on Windows, Linux and macOS
"""

import sys
import argparse
import requests
from typing import List


def get_file_job(job_id: str, api_url: str = "http://localhost:8000") -> dict:
    """Gets file job with file information"""
    try:
        response = requests.get(f"{api_url}/file-jobs/{job_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error getting file job: {e}")
        return None


def set_file_job_to_process(
    job_id: str, api_url: str = "http://localhost:8000"
) -> bool:
    """Sets file job status to TO_PROCESS"""
    try:
        response = requests.post(f"{api_url}/file-jobs/{job_id}/process")
        response.raise_for_status()
        print(f"✅ File job {job_id} set to TO_PROCESS status")
        return True
    except requests.RequestException as e:
        print(f"❌ Error setting file job to process: {e}")
        return False


def process_file_job(job_id: str, api_url: str = "http://localhost:8000") -> dict:
    """Processes file job"""
    try:
        response = requests.post(
            f"{api_url}/ocr/process-job", params={"job_id": job_id}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error processing file job: {e}")
        return None


def get_file_jobs_to_process(api_url: str = "http://localhost:8000") -> List[dict]:
    """Gets all file jobs with TO_PROCESS status"""
    try:
        response = requests.get(f"{api_url}/file-jobs/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error getting file jobs to process: {e}")
        return []


def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Manage file jobs processing")
    parser.add_argument(
        "command",
        choices=["get", "process", "set-to-process", "list"],
        help="Command to execute",
    )
    parser.add_argument("--job-id", help="File job ID")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API URL")

    args = parser.parse_args()

    if args.command == "get":
        if not args.job_id:
            print("❌ Job ID is required for get command")
            sys.exit(1)

        result = get_file_job(args.job_id, args.api_url)
        if result:
            print(f"✅ File job details: {result}")

    elif args.command == "set-to-process":
        if not args.job_id:
            print("❌ Job ID is required for set-to-process command")
            sys.exit(1)

        set_file_job_to_process(args.job_id, args.api_url)

    elif args.command == "process":
        if not args.job_id:
            print("❌ Job ID is required for process command")
            sys.exit(1)

        result = process_file_job(args.job_id, args.api_url)
        if result:
            print(f"✅ File job processed: {result}")

    elif args.command == "list":
        file_jobs = get_file_jobs_to_process(args.api_url)
        if file_jobs:
            print(f"📋 File jobs to process ({len(file_jobs)}):")
            for job in file_jobs:
                print(
                    f"  - {job['id']} (Status: {job['status']}, File: {job['file_id']})"
                )
        else:
            print("📋 No file jobs to process")


if __name__ == "__main__":
    main()
