"""
Retriever setup and vector store configuration.
"""

import os
import threading

from langchain_core.documents import Document
from langchain_core.tools import create_retriever_tool
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document as LangChainDocument

from src.memory.chathistory_sqlite import DocumentManager

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

FAISS_INDEX_DIR = os.environ.get("FAISS_INDEX_DIR", "faiss_index_persistent")

# Global in-memory vectorstore and lock
_global_vectorstore = None
_vectorstore_lock = threading.Lock()

def _get_or_create_vectorstore():
    global _global_vectorstore
    
    with _vectorstore_lock:
        if _global_vectorstore is not None:
            return _global_vectorstore
        
    try:
        if os.path.exists(FAISS_INDEX_DIR):
            _global_vectorstore = FAISS.load_local(
                FAISS_INDEX_DIR, 
                embeddings, 
                allow_dangerous_deserialization=True
            )
            print("Loaded persistent FAISS vectorstore")
        else:
            print("No persistent documents found, creating dummy vectorstore")
            dummy_doc = LangChainDocument(
                page_content="No documents have been uploaded yet. Please upload a document first.",
                metadata={"source": "initialization"}
            )
            _global_vectorstore = FAISS.from_documents(
                documents=[dummy_doc],
                embedding=embeddings
            )
    except Exception as e:
        print(f"Error loading FAISS vectorstore: {e}")
        dummy_doc = LangChainDocument(
            page_content="Error loading documents.",
            metadata={"source": "error"}
        )
        _global_vectorstore = FAISS.from_documents([dummy_doc], embedding=embeddings)
        
    return _global_vectorstore

def retriever_chain(chunks: list[Document]):
    """
    Initialize and store documents in a persistent FAISS vector database.
    """
    global _global_vectorstore
    try:
        new_vectorstore = FAISS.from_documents(
            documents=chunks,
            embedding=embeddings
        )

        vectorstore = _get_or_create_vectorstore()
        
        with _vectorstore_lock:
            # If it was a dummy, we can't easily "remove" the dummy, but we can just merge.
            # It's better to just merge.
            vectorstore.merge_from(new_vectorstore)
            vectorstore.save_local(FAISS_INDEX_DIR)
            
            print("FAISS vector store saved to disk with new documents")
            return True
    except Exception as e:
        print(f"Error storing documents in FAISS: {e}")
        return False

def remove_document_from_faiss(filename: str):
    """
    Remove all chunks from FAISS matching a filename.
    """
    global _global_vectorstore
    try:
        vectorstore = _get_or_create_vectorstore()
        
        # Find all doc IDs that match the filename
        ids_to_delete = []
        for doc_id, doc in vectorstore.docstore._dict.items():
            if doc.metadata.get("filename") == filename:
                ids_to_delete.append(doc_id)
                
        if ids_to_delete:
            with _vectorstore_lock:
                vectorstore.delete(ids_to_delete)
                vectorstore.save_local(FAISS_INDEX_DIR)
            print(f"Deleted {len(ids_to_delete)} chunks from FAISS for {filename}")
            return True
        return False
    except Exception as e:
        print(f"Error removing from FAISS: {e}")
        return False

def get_retriever():
    """
    Get a retriever tool connected to the persistent FAISS vector store.
    """
    try:
        vectorstore = _get_or_create_vectorstore()
        retriever = vectorstore.as_retriever()

        from langchain_core.prompts import PromptTemplate
        document_prompt = PromptTemplate.from_template(
            "[Source: {filename}, Page: {page}]\n{page_content}"
        )

        retriever_tool = create_retriever_tool(
            retriever,
            "retriever",
            "Search and retrieve information from the user's uploaded documents. Use this tool whenever the user asks a question about their uploaded files.",
            document_prompt=document_prompt
        )

        return retriever_tool

    except Exception as e:
        print(f"Error initializing retriever: {e}")
        raise Exception(e)
