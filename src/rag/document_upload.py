"""
Document upload and processing module.
"""

import os
import tempfile

from fastapi import UploadFile, File
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.rag.retriever_setup import retriever_chain
from src.tools.common_tools import enhance_description_with_llm
from src.memory.chathistory_sqlite import DocumentManager


def documents(description: str, file: UploadFile = File(...)):
    """
    Process and upload a document for RAG.

    Validates file type, loads content, enhances description, chunks documents,
    and stores them in the vector database.

    Args:
        description: User-provided document description.
        file: The uploaded file (PDF or TXT).

    Returns:
        Boolean indicating success of the upload process.

    Raises:
        HTTPException: If file type is not supported or loading fails.
    """
    filename = file.filename
    print(filename)
    if not filename.endswith(".pdf") and not filename.endswith(".txt"):
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="Only PDF and TXT files are supported"
        )

    file_bytes = file.file.read()

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=os.path.splitext(filename)[1]
    ) as tmp_file:
        tmp_file.write(file_bytes)
        tmp_path = tmp_file.name

    if filename.endswith(".pdf"):
        loader = PyPDFLoader(tmp_path)
    else:
        loader = TextLoader(tmp_path, encoding="utf-8")

    try:
        docs = loader.load()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=500,
            detail=f"Error loading file: {e}"
        )
    finally:
        os.unlink(tmp_path)

    # Enhance description using LLM
    description_llm = enhance_description_with_llm(description)

    # Save enhanced description to SQLite
    DocumentManager.add_document(filename, description_llm)

    print(f"Document {filename} added to SQLite with description: {description_llm}")

    import re
    # Normalize text to remove excessive whitespace and clean up PDF extractions
    for doc in docs:
        if doc.page_content:
            doc.page_content = re.sub(r'\s+', ' ', doc.page_content).strip()

    # Split documents into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    chunks = splitter.split_documents(docs)
    
    if not chunks:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=400,
            detail="No readable text found in the document. Is it a scanned PDF?"
        )
    
    # Add filename and ensure page metadata exists for all chunks
    for chunk in chunks:
        chunk.metadata["filename"] = filename
        if "page" not in chunk.metadata:
            chunk.metadata["page"] = 1 # TXT files or un-paginated PDFs default to 1
        else:
            # PyPDFLoader is 0-indexed, let's make it 1-indexed for humans
            chunk.metadata["page"] += 1

    return retriever_chain(chunks)




