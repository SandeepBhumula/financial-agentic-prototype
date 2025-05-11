# Vector Database Setup

This package handles the setup, configuration, and usage of ChromaDB as a vector database for healthcare financial data.

## Overview

The vector database implementation provides semantic search capabilities for financial and healthcare data, allowing the application to find and retrieve relevant information based on user queries.

## Files and Components

- `chroma_setup.py`: Core implementation for ChromaDB setup, configuration, and data retrieval
- `document_chunking.py`: Logic for processing and chunking data for efficient vector storage
- `populate_vector_db.py`: Script to populate the vector database with data
- `run_setup.py`: CLI script to run the setup process
- `vector_db_factory.py`: Factory implementation that provides a clean interface to the vector database

## Configuration

The vector database can be configured in two ways:

### 1. Local/Persistent Mode

For development and standalone usage, ChromaDB can operate with local persistent storage:

```env
CHROMA_PERSIST_DIRECTORY=./data/chroma_db
CHROMA_USE_PERSISTENT=true
```

### 2. Server Mode

For containerized environments or when you need a separate ChromaDB server:

```env
CHROMA_HOST=chroma-db
CHROMA_PORT=8100
CHROMA_USE_PERSISTENT=false
```

## Usage

### Basic Usage

To get the vector store:

```python
from vector_db.vector_db_factory import get_vector_store

# Get the vector store
vector_store = get_vector_store()

# Search for documents
results = vector_store.similarity_search("What is a Health Savings Account?", k=3)
```

### Setup Vector Database

To populate the vector database with data:

```python
from vector_db.vector_db_factory import setup_vector_store

# Set up the vector store (with optional reset)
success = setup_vector_store(reset=True)
```

### Reset Vector Database

To reset the vector database:

```python
from vector_db.vector_db_factory import reset_vector_store

# Reset the vector store
success = reset_vector_store()
```

## Docker Integration

When using the vector database in Docker, ensure the ChromaDB service is properly configured in your `docker-compose.yml`:

```yaml
services:
  chroma-db:
    container_name: chroma-db
    image: chromadb/chroma:latest
    volumes:
      - chroma-data:/chroma/chroma
    environment:
      - ALLOW_RESET=True
      - ANONYMIZED_TELEMETRY=False
    ports:
      - "8100:8100"
    command: uvicorn chromadb.app:app --host 0.0.0.0 --port 8100
```

And set the environment variables in your application service:

```yaml
  app:
    environment:
      - CHROMA_HOST=chroma-db
      - CHROMA_PORT=8100
      - CHROMA_USE_PERSISTENT=false
```

## API Implementation Notes

- In server mode, the REST API implementation is used
- In persistent mode, the default local implementation is used

## Troubleshooting

If you encounter issues with the vector database, try the following:

1. Check that the ChromaDB server is running (for server mode)
2. Ensure the CHROMA_HOST and CHROMA_PORT are correctly set
3. Try resetting the vector database to rebuild the indexes
4. Check the logs for detailed error messages 