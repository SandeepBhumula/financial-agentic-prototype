#!/usr/bin/env python3
"""
Test script to verify that the vector database has been properly initialized.
This can be run after the Docker containers are up to check if the vector DB setup worked.
"""

import os
import sys
import logging
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_vector_store():
    """Test that the vector store is properly initialized and can be queried."""
    try:
        # Import the vector store factory
        from vector_db.vector_db_factory import get_vector_store
        
        # Get the vector store
        logger.info("Getting vector store...")
        vector_store = get_vector_store()
        
        if vector_store is None:
            logger.error("Failed to get vector store")
            return False
        
        # Try a simple query
        logger.info("Testing vector store with a simple query...")
        results = vector_store.similarity_search("What is a Health Savings Account?", k=2)
        
        if not results:
            logger.warning("Query returned no results")
            return False
        
        # Print the results
        logger.info(f"Query returned {len(results)} results")
        for i, doc in enumerate(results):
            logger.info(f"Result {i+1}:")
            logger.info(f"  Content: {doc.page_content[:100]}...")
            logger.info(f"  Metadata: {doc.metadata}")
        
        logger.info("Vector store test completed successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error testing vector store: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting vector database test")
    success = test_vector_store()
    
    if success:
        logger.info("Vector database is properly initialized and working")
        sys.exit(0)
    else:
        logger.error("Vector database test failed")
        sys.exit(1) 