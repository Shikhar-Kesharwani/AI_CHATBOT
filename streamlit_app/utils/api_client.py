"""
API client for communicating with backend services.
"""

import logging
import os

import requests

logger = logging.getLogger(__name__)

PYTHON_BASE_URL = "http://127.0.0.1:8000"


def get_documents_rag() -> list:
    """Fetch all active documents from the backend."""
    url = f"{PYTHON_BASE_URL}/rag/documents"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Failed to fetch documents: {e}")
        return []

def get_chat_history_rag(session_id: str) -> list:
    """Fetch chat history for the current session."""
    url = f"{PYTHON_BASE_URL}/rag/history/{session_id}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        logger.error(f"Failed to fetch chat history: {e}")
        return []


def query_backend(query: str, session_id: str) -> str:
    """
    Send a query to the RAG backend.

    Args:
        query: The user's query text.
        session_id: Session identifier for tracking conversation.

    Returns:
        Response text from the backend or error message.
    """
    url = f"{PYTHON_BASE_URL}/rag/query"
    print(f"[query_backend] Calling: {url}")

    response = requests.post(
        url,
        json={"query": query, "session_id": session_id},
        stream=True
    )

    if response.status_code == 200:
        for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
            if chunk:
                yield chunk
    else:
        yield f"Error: {response.status_code} - {response.text}"


def document_upload_rag(file, description: str) -> bool:
    """
    Upload a document to the RAG system.

    Args:
        file: File object to upload.
        description: Description of the document.

    Returns:
        True if upload succeeds, False otherwise.
    """
    headers = {
        "X-Description": description
    }
    url = f"{PYTHON_BASE_URL}/rag/documents/upload"

    if file:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(url, files=files, headers=headers)
        print(response)

        if response.status_code == 200:
            return True

    return False


def delete_document_rag(filename: str) -> bool:
    """
    Delete a document from the RAG system.
    """
    url = f"{PYTHON_BASE_URL}/rag/documents/delete/{filename}"
    try:
        response = requests.delete(url)
        if response.status_code == 200:
            return True
        return False
    except Exception as e:
        print(f"Delete failed: {e}")
        return False
