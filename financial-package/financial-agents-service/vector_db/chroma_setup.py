#!/usr/bin/env python3
"""
ChromaDB Vector Database Setup

This module handles setting up and configuring ChromaDB for 
vector search of healthcare financial data.
"""

import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import chromadb
from chromadb.config import Settings
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

from vector_db.document_chunking import process_data_for_vectorization

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY", 
                                          os.path.join(Path(__file__).parent.parent, "data", "chroma_db"))
USE_PERSISTENT = os.environ.get("CHROMA_USE_PERSISTENT", "true").lower() == "true"
COLLECTION_NAME = "healthcare_financial_data"
EMBEDDING_MODEL = "text-embedding-3-large"  # OpenAI's text embedding model

def get_chroma_client():
    """
    Create and return a ChromaDB client with the configured settings.
    """
    try:
        if USE_PERSISTENT:
            # Ensure persist directory exists
            os.makedirs(CHROMA_PERSIST_DIRECTORY, exist_ok=True)
            
            # Create persistent client
            client = chromadb.PersistentClient(
                path=CHROMA_PERSIST_DIRECTORY,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            logger.info(f"Created persistent ChromaDB client at {CHROMA_PERSIST_DIRECTORY}")
        else:
            # Create HTTP client (for server mode)
            client = chromadb.HttpClient(
                host=CHROMA_HOST,
                port=CHROMA_PORT,
                settings=Settings(
                    allow_reset=True,
                    anonymized_telemetry=False
                )
            )
            logger.info(f"Connected to ChromaDB server at {CHROMA_HOST}:{CHROMA_PORT}")
        
        return client
    except Exception as e:
        logger.error(f"Error connecting to ChromaDB: {str(e)}")
        return None

def get_collection(client):
    """
    Get or create the collection for healthcare financial data.
    """
    try:
        # Check if collection exists
        collections = client.list_collections()
        collection_names = [collection.name for collection in collections]
        
        if COLLECTION_NAME in collection_names:
            collection = client.get_collection(name=COLLECTION_NAME)
            logger.info(f"Using existing collection: {COLLECTION_NAME}")
        else:
            # Create new collection
            collection = client.create_collection(
                name=COLLECTION_NAME,
                metadata={"description": "Healthcare financial data"}
            )
            logger.info(f"Created new collection: {COLLECTION_NAME}")
        
        return collection
    except Exception as e:
        logger.error(f"Error getting collection: {str(e)}")
        return None

def get_openai_embeddings():
    """
    Initialize and return the OpenAI embeddings model.
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable is not set")
        return None
    
    try:
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        return embeddings
    except Exception as e:
        logger.error(f"Error initializing OpenAI embeddings: {str(e)}")
        return None

def index_documents(documents: List[Document], embeddings) -> bool:
    """
    Index documents into ChromaDB using LangChain's Chroma integration.
    
    Args:
        documents: List of Document objects to index
        embeddings: Embedding model to use
        
    Returns:
        bool: True if successful, False otherwise
    """
    if not documents or embeddings is None:
        logger.error("Cannot index documents - missing required parameters")
        return False
    
    try:
        # Create LangChain Chroma vector store
        vector_store = get_vector_store(embeddings)
        if not vector_store:
            return False
        
        # Add documents to the vector store
        logger.info(f"Indexing {len(documents)} documents into ChromaDB")
        vector_store.add_documents(documents)
        
        # Persist if using persistent mode
        if USE_PERSISTENT:
            vector_store.persist()
        
        logger.info(f"Successfully indexed {len(documents)} documents")
        return True
    except Exception as e:
        logger.error(f"Error indexing documents: {str(e)}")
        return False

def get_vector_store(embeddings=None):
    """
    Get the ChromaDB vector store with healthcare financial data.
    
    Args:
        embeddings: Optional embeddings model to use. If None, a new one will be created.
        
    Returns:
        Chroma vector store instance or None if failed
    """
    if embeddings is None:
        embeddings = get_openai_embeddings()
        if embeddings is None:
            return None
    
    try:
        # Set the appropriate implementation based on environment
        if USE_PERSISTENT:
            # For local persistent mode
            logger.info(f"Initializing local ChromaDB at {CHROMA_PERSIST_DIRECTORY}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
        else:
            # For server/containerized mode using REST API
            logger.info(f"Initializing ChromaDB with REST API at {CHROMA_HOST}:{CHROMA_PORT}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                client_settings=chromadb.config.Settings(
                    chroma_api_impl="rest",
                    chroma_server_host=CHROMA_HOST,
                    chroma_server_http_port=CHROMA_PORT,
                    anonymized_telemetry=False
                )
            )
        
        # Check if vector store has data
        collection_data = vector_store.get()
        if collection_data and len(collection_data.get('ids', [])) > 0:
            logger.info(f"Using existing vector store with {len(collection_data['ids'])} documents")
        else:
            logger.warning("Vector store exists but contains no documents")
        
        return vector_store
    except Exception as e:
        logger.error(f"Error getting vector store: {str(e)}")
        return None

def reset_vector_store():
    """
    Reset the vector store by deleting and recreating the collection.
    """
    try:
        client = get_chroma_client()
        if client is None:
            return False
        
        # Delete collection if it exists
        collections = client.list_collections()
        collection_names = [collection.name for collection in collections]
        
        if COLLECTION_NAME in collection_names:
            client.delete_collection(name=COLLECTION_NAME)
            logger.info(f"Deleted collection: {COLLECTION_NAME}")
        
        # Create new collection
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Healthcare financial data"}
        )
        logger.info(f"Created new collection: {COLLECTION_NAME}")
        
        return True
    except Exception as e:
        logger.error(f"Error resetting vector store: {str(e)}")
        return False

def setup_vector_store(reset=False):
    """
    Main function to set up the ChromaDB vector store with healthcare financial data.
    
    Args:
        reset: Whether to reset the vector store before setup
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Step 1: Reset vector store if requested
    if reset:
        if not reset_vector_store():
            return False
    
    # Step 2: Get the OpenAI embeddings model
    embeddings = get_openai_embeddings()
    if not embeddings:
        return False
    
    # Step 3: Process the data into chunks
    chunks = process_data_for_vectorization()
    if not chunks:
        logger.error("No document chunks to index")
        return False
    
    # Step 4: Index the chunks
    return index_documents(chunks, embeddings)

if __name__ == "__main__":
    logger.info("--- Starting ChromaDB Vector DB Setup ---")
    
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable must be set")
    else:
        success = setup_vector_store(reset=True)
        if success:
            logger.info("Vector DB setup completed successfully")
        else:
            logger.error("Vector DB setup failed")
    
    logger.info("--- ChromaDB Vector DB Setup Complete ---") 