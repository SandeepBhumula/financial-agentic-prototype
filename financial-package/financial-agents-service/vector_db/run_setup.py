#!/usr/bin/env python3
"""
Run the complete setup process for the vector database:
1. Generate synthetic healthcare financial data
2. Create document chunks
3. Generate embeddings
4. Load data into ChromaDB
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

def main():
    """Run the complete vector database setup process"""
    logger.info("Starting vector database setup process")
    
    try:
        # Step 1: Generate synthetic data
        logger.info("Step 1: Generating synthetic healthcare financial data")
        from scripts.generate_synthetic_data import generate_synthetic_data
        accounts, transactions = generate_synthetic_data()
        logger.info(f"Generated {len(accounts)} accounts and {len(transactions)} transactions")
        
        # Step 2: Create document chunks from the generated data
        logger.info("Step 2: Creating document chunks")
        from vector_db.document_chunking import process_data_for_vectorization
        chunks = process_data_for_vectorization()
        if not chunks:
            logger.error("Failed to create document chunks")
            return False
        logger.info(f"Created {len(chunks)} document chunks")
        
        # Step 3: Set up ChromaDB and load the chunks
        logger.info("Step 3: Setting up ChromaDB and loading data")
        # Check if we need ChromaDB configuration
        if "CHROMA_HOST" not in os.environ:
            logger.info("CHROMA_HOST environment variable not set. Using persistent mode.")
            
        from vector_db.chroma_setup import setup_vector_store
        success = setup_vector_store(reset=True)
        if not success:
            logger.error("Failed to set up vector store")
            return False
        
        logger.info("Vector database setup completed successfully")
        
        # Optional: Test the knowledge agent with the new vector store
        logger.info("Testing knowledge agent with the new vector store")
        from core.knowledge import handle_query
        
        test_queries = [
            "What is the contribution limit for an HSA in 2024?",
            "Can I use my FSA for vision care?",
            "What's the difference between an HSA and FSA?",
            "Am I eligible for an HSA if I have Medicare?",
            "How does a prepaid healthcare card work?"
        ]
        
        for query in test_queries:
            logger.info(f"Testing query: {query}")
            response = handle_query(query)
            logger.info(f"Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during vector database setup: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        logger.info("Setup completed successfully")
    else:
        logger.error("Setup failed")
        sys.exit(1) 