#!/usr/bin/env python3
"""
Script to manage document processing
Works on Windows, Linux and macOS
"""

import sys
import argparse
import requests
from typing import List


def create_document(
    url: str, filename: str, api_url: str = "http://localhost:8000"
) -> dict:
    """Creates a new document record"""
    try:
        response = requests.post(
            f"{api_url}/documents/", json={"url": url, "filename": filename}
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error creating document: {e}")
        return None


def set_document_to_process(url: str, api_url: str = "http://localhost:8000") -> bool:
    """Sets document status to TO_PROCESS"""
    try:
        response = requests.post(f"{api_url}/documents/{url}/process")
        response.raise_for_status()
        print(f"✅ Document {url} set to TO_PROCESS status")
        return True
    except requests.RequestException as e:
        print(f"❌ Error setting document to process: {e}")
        return False


def process_document(url: str, api_url: str = "http://localhost:8000") -> dict:
    """Processes document from URL"""
    try:
        response = requests.post(f"{api_url}/ocr/process-url", params={"url": url})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error processing document: {e}")
        return None


def get_document_status(url: str, api_url: str = "http://localhost:8000") -> dict:
    """Gets document status"""
    try:
        response = requests.get(f"{api_url}/documents/{url}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error getting document status: {e}")
        return None


def get_documents_to_process(api_url: str = "http://localhost:8000") -> List[dict]:
    """Gets all documents with TO_PROCESS status"""
    try:
        response = requests.get(f"{api_url}/documents/")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"❌ Error getting documents to process: {e}")
        return []


def main():
    """Main script function"""
    parser = argparse.ArgumentParser(description="Manage document processing")
    parser.add_argument(
        "command",
        choices=["create", "process", "status", "set-to-process", "list"],
        help="Command to execute",
    )
    parser.add_argument("--url", help="Document URL")
    parser.add_argument("--filename", help="Document filename")
    parser.add_argument("--api-url", default="http://localhost:8000", help="API URL")

    args = parser.parse_args()

    if args.command == "create":
        if not args.url or not args.filename:
            print("❌ URL and filename are required for create command")
            sys.exit(1)

        result = create_document(args.url, args.filename, args.api_url)
        if result:
            print(f"✅ Document created: {result}")

    elif args.command == "set-to-process":
        if not args.url:
            print("❌ URL is required for set-to-process command")
            sys.exit(1)

        set_document_to_process(args.url, args.api_url)

    elif args.command == "process":
        if not args.url:
            print("❌ URL is required for process command")
            sys.exit(1)

        result = process_document(args.url, args.api_url)
        if result:
            print(f"✅ Document processed: {result}")

    elif args.command == "status":
        if not args.url:
            print("❌ URL is required for status command")
            sys.exit(1)

        result = get_document_status(args.url, args.api_url)
        if result:
            print(f"�� Document status: {result}")

    elif args.command == "list":
        documents = get_documents_to_process(args.api_url)
        if documents:
            print(f"📋 Documents to process ({len(documents)}):")
            for doc in documents:
                print(f"  - {doc['url']} ({doc['status']})")
        else:
            print("📋 No documents to process")


if __name__ == "__main__":
    main()
