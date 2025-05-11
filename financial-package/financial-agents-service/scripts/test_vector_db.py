#!/usr/bin/env python3
"""
Test script for ChromaDB vector database functionality.
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import required modules
from dotenv import load_dotenv
load_dotenv()

from vector_db.chroma_setup import get_openai_embeddings, get_vector_store, reset_vector_store
from core.knowledge import handle_query

def test_vector_store():
    """
    Test the ChromaDB vector store setup and functionality.
    """
    logger.info("Starting ChromaDB test")
    
    # Step 1: Check if embeddings can be initialized
    logger.info("Testing embeddings initialization...")
    embeddings = get_openai_embeddings()
    if embeddings is None:
        logger.error("Failed to initialize embeddings")
        return False
    logger.info("Embeddings initialized successfully")
    
    # Step 2: Test vector store access
    logger.info("Testing vector store access...")
    vector_store = get_vector_store(embeddings)
    if vector_store is None:
        logger.error("Failed to access vector store")
        return False
    logger.info("Vector store accessed successfully")
    
    # Step 3: Test simple search
    logger.info("Testing similarity search...")
    try:
        query = "What is an HSA?"
        results = vector_store.similarity_search(query, k=2)
        logger.info(f"Found {len(results)} results for query: '{query}'")
        
        if results:
            logger.info(f"Sample result: {results[0].page_content[:100]}...")
            logger.info(f"Metadata: {results[0].metadata}")
        else:
            logger.warning("No results found. Vector store might be empty.")
    except Exception as e:
        logger.error(f"Error during similarity search: {e}")
        return False
    
    # Step 4: Test the knowledge agent with the vector store
    logger.info("Testing knowledge agent integration...")
    
    test_queries = [
        "What is the contribution limit for an HSA in 2024?",
        "Can I use my FSA for vision care?",
        "What's the difference between an HSA and FSA?",
        "Am I eligible for an HSA if I have Medicare?",
        "How does a prepaid healthcare card work?"
    ]
    
    for query in test_queries:
        logger.info(f"Testing query: '{query}'")
        try:
            response = handle_query(query)
            logger.info(f"Response: {response[:100]}...")
        except Exception as e:
            logger.error(f"Error processing query '{query}': {e}")
    
    logger.info("ChromaDB test completed successfully")
    return True

if __name__ == "__main__":
    # Check if reset flag was passed
    reset = "--reset" in sys.argv
    
    if reset:
        logger.info("Resetting vector store before testing")
        reset_vector_store()
    
    success = test_vector_store()
    
    if success:
        logger.info("All tests completed successfully")
        sys.exit(0)
    else:
        logger.error("Tests failed")
        sys.exit(1) 