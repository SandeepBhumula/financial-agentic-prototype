#!/bin/bash
set -e

# Initialize logging
echo "$(date -u) - Starting docker-entrypoint.sh"

# Wait for ChromaDB service to be ready
echo "Waiting for ChromaDB to be ready..."
while ! curl -s http://${CHROMA_HOST:-chroma-db}:${CHROMA_PORT:-8100}/api/v1/heartbeat > /dev/null; do
    echo "ChromaDB not ready yet - sleeping for 2 seconds"
    sleep 2
done
echo "ChromaDB is ready!"

# Check if we need to run the vector DB setup
if [ "${INITIALIZE_VECTOR_DB:-true}" = "true" ]; then
    echo "Initializing vector database..."
    python -m vector_db.run_setup
    
    # Store a flag file to indicate setup has been run
    mkdir -p /app/data
    touch /app/data/vector_db_initialized
    echo "Vector database initialization complete!"
else
    echo "Skipping vector database initialization (INITIALIZE_VECTOR_DB=false)"
fi

# Execute the command provided as arguments (the default is to run the FastAPI app)
echo "Starting main application..."
exec "$@" 