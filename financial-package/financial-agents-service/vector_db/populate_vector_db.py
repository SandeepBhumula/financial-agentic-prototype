#!/usr/bin/env python3
"""
Populate Vector Database

This script populates the Chroma vector database with healthcare financial data.
It processes the data from various sources, creates chunks, and generates embeddings.
"""

import os
import sys
import json
import logging
from pathlib import Path

# Add parent directory to import path
sys.path.append(str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import services
from vector_db.document_chunking import process_data_for_vectorization
from vector_db.chroma_setup import setup_vector_store

def populate_db(reset=False):
    """
    Populate the Vector DB with healthcare financial data.
    
    Args:
        reset: Whether to reset the database before populating
        
    Returns:
        bool: True if operation was successful
    """
    logger.info("Starting Vector DB population process")
    
    # Check for required environment variables
    if "OPENAI_API_KEY" not in os.environ:
        logger.error("OPENAI_API_KEY environment variable is not set")
        return False
    
    try:
        # Step 1: Create vector store (this will automatically reset if requested)
        success = setup_vector_store(reset=reset)
        
        if success:
            logger.info("Vector DB successfully populated")
            
            # Create a flag file to indicate successful population
            flag_path = os.path.join(Path(__file__).parent.parent, "data", "vector_store_populated.flag")
            with open(flag_path, "w") as f:
                f.write(f"Vector store populated successfully at {Path(__file__).name}")
                
            return True
        else:
            logger.error("Failed to populate vector DB")
            return False
            
    except Exception as e:
        logger.error(f"Error during vector DB population: {e}")
        return False

if __name__ == "__main__":
    # Check if reset flag was passed
    reset = "--reset" in sys.argv
    
    if reset:
        logger.info("Will reset the vector DB before populating")
    
    # Populate the DB
    success = populate_db(reset=reset)
    
    if success:
        logger.info("Vector DB population completed successfully")
        sys.exit(0)
    else:
        logger.error("Vector DB population failed")
        sys.exit(1) 