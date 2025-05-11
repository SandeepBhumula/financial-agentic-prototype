#!/usr/bin/env python3
"""
Vector Database Factory

This module provides a factory pattern for ChromaDB vector database implementation.
It encapsulates the setup, access, and management of the ChromaDB vector store.
"""

import os
import logging
from typing import Optional
from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_vector_store(embeddings=None):
    """
    Factory method to get the ChromaDB vector store.
    
    Args:
        embeddings: Optional embeddings model to use
        
    Returns:
        The vector store instance or None if failed
    """
    # Initialize embeddings if not provided
    if embeddings is None:
        try:
            embeddings = OpenAIEmbeddings(
                model=os.environ.get("EMBEDDING_MODEL", "text-embedding-3-large"),
                openai_api_key=os.environ.get("OPENAI_API_KEY")
            )
        except Exception as e:
            logger.error(f"Error initializing embeddings: {e}")
            return None
    
    try:
        from vector_db.chroma_setup import get_vector_store as get_chroma_store
        return get_chroma_store(embeddings)
    except Exception as e:
        logger.error(f"Error getting Chroma vector store: {e}")
        return None

def setup_vector_store(reset=False):
    """
    Factory method to set up the ChromaDB vector store.
    
    Args:
        reset: Whether to reset the vector store before setup
        
    Returns:
        True if successful, False otherwise
    """
    try:
        from vector_db.chroma_setup import setup_vector_store as setup_chroma
        return setup_chroma(reset)
    except Exception as e:
        logger.error(f"Error setting up Chroma vector store: {e}")
        return False

def reset_vector_store():
    """
    Factory method to reset the ChromaDB vector store.
    
    Returns:
        True if successful, False otherwise
    """
    try:
        from vector_db.chroma_setup import reset_vector_store as reset_chroma
        return reset_chroma()
    except Exception as e:
        logger.error(f"Error resetting Chroma vector store: {e}")
        return False

if __name__ == "__main__":
    # Simple test to verify the factory is working
    vector_store = get_vector_store()
    if vector_store:
        logger.info("Successfully initialized vector store")
    else:
        logger.error("Failed to initialize vector store") 