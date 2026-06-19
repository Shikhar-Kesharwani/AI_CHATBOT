"""
API routes for RAG operations.
"""

from fastapi import APIRouter, UploadFile, File, Header
from fastapi.responses import StreamingResponse
import asyncio
from langchain_core.messages import HumanMessage, AIMessage

from src.memory.chathistory_sqlite import SQLiteChatMessageHistory
from src.models.query_request import QueryRequest
from src.rag.document_upload import documents
from src.rag.graph_builder import builder

router = APIRouter()


@router.post("/rag/query")
async def rag_query(req: QueryRequest):
    """
    Process a RAG query and return the result.

    Args:
        req: The query request containing query text and session_id.

    Returns:
        The generated response from the RAG pipeline.
    """
    chat_history = SQLiteChatMessageHistory(req.session_id)
    chat_history.add_message(HumanMessage(content=req.query))
    messages = chat_history.messages

    async def stream_generator():
        output_text = ""
        try:
            # Run graph in stream mode to capture intermediate agent steps
            for event in builder.stream({"messages": messages}, stream_mode="updates"):
                for node_name, state_update in event.items():
                    yield f"__NODE__{node_name}|||"
                    await asyncio.sleep(0.05)
                    
                    if "messages" in state_update:
                        msgs = state_update["messages"]
                        if isinstance(msgs, list) and len(msgs) > 0:
                            last_msg = msgs[-1]
                            output_text = last_msg.get("content", "") if isinstance(last_msg, dict) else getattr(last_msg, "content", str(last_msg))
                        else:
                            output_text = msgs.get("content", "") if isinstance(msgs, dict) else getattr(msgs, "content", str(msgs))

            # Save assistant message to SQLite
            chat_history.add_message(AIMessage(content=output_text))

            # Stream the output chunk by chunk to simulate typing
            words = output_text.split(" ")
            for i, word in enumerate(words):
                yield word + (" " if i < len(words) - 1 else "")
                await asyncio.sleep(0.02)
        except Exception as e:
            # Gracefully handle the error and stream it to the frontend
            error_msg = f"\n\n**Error:** The backend encountered a problem: {str(e)}"
            yield error_msg
            chat_history.add_message(AIMessage(content=error_msg))

    return StreamingResponse(stream_generator(), media_type="text/plain")


@router.post("/rag/documents/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Header(..., alias="X-Description")
):
    """
    Upload a document for RAG processing.

    Args:
        file: The file to upload (PDF or TXT).
        description: Document description provided via header.

    Returns:
        Upload status.
    """
    status_upload = documents(description, file)
    return {"status": status_upload}


@router.delete("/rag/documents/delete/{filename}")
async def delete_document_endpoint(filename: str):
    from src.memory.chathistory_sqlite import DocumentManager
    from src.rag.retriever_setup import remove_document_from_faiss
    
    # 1. Delete from SQLite
    DocumentManager.delete_document(filename)
    
    # 2. Delete from FAISS
    remove_document_from_faiss(filename)
    
    return {"status": "success"}


@router.get("/rag/documents")
async def get_documents():
    """Fetch all active documents."""
    from src.memory.chathistory_sqlite import DocumentManager
    return DocumentManager.get_all_documents()

@router.get("/rag/history/{session_id}")
async def get_chat_history(session_id: str):
    """Fetch chat history for a session."""
    chat_history = SQLiteChatMessageHistory(session_id)
    # Convert BaseMessage to dictionaries
    return [{"role": msg.type, "content": msg.content} for msg in chat_history.messages]

