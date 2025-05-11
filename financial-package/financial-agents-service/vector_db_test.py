#!/usr/bin/env python3

"""
Vector Store Test Script
Shows direct usage of the vector store with REST API implementation
"""

import os
import json
import logging
from pathlib import Path

import pandas as pd
import chromadb
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY", 
                                         os.path.join(Path(__file__).parent, "data", "chroma_db"))
USE_PERSISTENT = os.environ.get("CHROMA_USE_PERSISTENT", "true").lower() == "true"
COLLECTION_NAME = "healthcare_financial_data"

EMBEDDING_MODEL = "text-embedding-3-large"
DATA_DIR = os.path.join(Path(__file__).parent, 'data')

def get_embedding_client():
    """
    Get the OpenAI embeddings client
    """
    if not OPENAI_API_KEY:
        logger.error("OPENAI_API_KEY environment variable is not set")
        print("⚠️ Error: OPENAI_API_KEY is not set. Please set it in your environment.")
        return None
    
    try:
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        logger.info("Successfully initialized OpenAI embeddings client")
        print("✅ Successfully initialized OpenAI embeddings client")
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embeddings client: {e}")
        print(f"⚠️ Error initializing OpenAI embeddings: {e}")
        return None

def get_vector_store_fixed():
    """
    Get ChromaDB vector store with proper API implementation
    """
    # Get embeddings client
    embeddings = get_embedding_client()
    if not embeddings:
        logger.error("Cannot get vector store - embeddings client initialization failed")
        print("Cannot get vector store - embeddings client initialization failed")
        return None
    
    # Initialize the vector store with REST API implementation for Docker environment
    try:
        # For Docker/containerized environment, use REST API
        if not USE_PERSISTENT:
            logger.info(f"Initializing ChromaDB with REST API at {CHROMA_HOST}:{CHROMA_PORT}")
            print(f"Initializing ChromaDB with REST API at {CHROMA_HOST}:{CHROMA_PORT}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                client_settings=chromadb.config.Settings(
                    chroma_api_impl="rest",  # Use REST API instead of duckdb+parquet
                    chroma_server_host=CHROMA_HOST,
                    chroma_server_http_port=CHROMA_PORT,
                    anonymized_telemetry=False
                )
            )
        else:
            # For local/persistent mode
            logger.info(f"Initializing local ChromaDB at {CHROMA_PERSIST_DIRECTORY}")
            print(f"Initializing local ChromaDB at {CHROMA_PERSIST_DIRECTORY}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
        
        logger.info("Vector store initialized successfully")
        print("✅ Vector store initialized successfully")
        return vector_store
    
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        print(f"❌ Failed to initialize vector store: {e}")
        return None

def get_mock_results(query):
    """Provide mock results when vector store is unavailable"""
    logger.info("Using mock data as fallback since vector store is unavailable")
    print("Using mock data as fallback since vector store is unavailable")
    
    if "hsa" in query.lower() or "health savings" in query.lower():
        return [{
            "text": "Health Savings Account (HSA) is a tax-advantaged savings account for individuals with high-deductible health plans. The 2024 contribution limit for individuals is $4,150 and for families is $8,300.",
            "source": "healthcare_products",
            "product_id": "HSA001",
            "product_name": "Health Savings Account (HSA)"
        }]
    elif "fsa" in query.lower() or "flexible spending" in query.lower():
        return [{
            "text": "Flexible Spending Account (FSA) is an employer-sponsored account allowing employees to set aside pre-tax dollars for eligible healthcare expenses. The 2024 contribution limit is $3,200.",
            "source": "healthcare_products",
            "product_id": "FSA001",
            "product_name": "Flexible Spending Account (FSA)"
        }]
    else:
        return [{
            "text": "Healthcare financial products include HSAs, FSAs, Dependent Care accounts, and Prepaid cards. Each has different eligibility requirements and benefits.",
            "source": "healthcare_products",
            "product_id": "",
            "product_name": ""
        }]

def query_knowledge(question, use_fallback=True):
    """Query knowledge with fallback to mock data if needed"""
    logger.info(f"Processing query: '{question}'")
    print(f"Processing query: '{question}'")
    
    # Try vector store first
    try:
        vector_store = get_vector_store_fixed()
        if vector_store:
            results = vector_store.similarity_search(question, k=3)
            if results:
                logger.info("Retrieved results from vector store")
                print("✅ Retrieved results from vector store")
                for i, doc in enumerate(results):
                    print(f"\nResult {i+1}:")
                    print(f"Source: {doc.metadata.get('source', 'unknown')}")
                    if doc.metadata.get('product_name'):
                        print(f"Product: {doc.metadata.get('product_name')}")
                    print(f"Text: {doc.page_content[:150]}...")
                return results
    except Exception as e:
        logger.error(f"Vector store query failed: {e}")
        print(f"⚠️ Vector store query failed: {e}")
    
    # Fall back to mock data if needed and allowed
    if use_fallback:
        logger.info("Falling back to mock data")
        print("Falling back to mock data")
        mock_results = get_mock_results(question)
        print("\nMock results:")
        for result in mock_results:
            print(f"Product: {result.get('product_name', 'N/A')}")
            print(f"Text: {result['text']}")
        return mock_results
    
    logger.warning("No results found and fallback disabled")
    print("❌ No results found and fallback disabled")
    return []

def run_demos():
    """Run a series of demonstration queries"""
    print("\n" + "="*50)
    print("VECTOR STORE DIRECT USAGE DEMO")
    print("="*50 + "\n")
    
    # Configuration info
    print("Configuration:")
    print(f"  - Host: {CHROMA_HOST}")
    print(f"  - Port: {CHROMA_PORT}")
    print(f"  - Persistent: {USE_PERSISTENT}")
    print(f"  - Data directory: {DATA_DIR}")
    print(f"  - OpenAI API Key: {'Set' if OPENAI_API_KEY else 'Not Set'}")
    
    # Demo 1: HSA query
    print("\n" + "-"*50)
    print("DEMO 1: HSA Information Query")
    print("-"*50)
    query_knowledge("What are the contribution limits for HSA accounts in 2024?")
    
    # Demo 2: FSA query
    print("\n" + "-"*50)
    print("DEMO 2: FSA Information Query")
    print("-"*50)
    query_knowledge("Tell me about Flexible Spending Accounts")
    
    # Demo 3: Generic query
    print("\n" + "-"*50)
    print("DEMO 3: General Healthcare Finance Query")
    print("-"*50)
    query_knowledge("What healthcare financial accounts are available to me?")
    
    print("\n" + "="*50)
    print("DEMO COMPLETE")
    print("="*50)

if __name__ == "__main__":
    run_demos() 