# Financial Agents Package

This package contains LangGraph-based financial AI agents and API services for interacting with them.

## Components

- **Knowledge Agent**: Provides informational responses about financial products
- **Card Agent**: Handles card operations like activation and deactivation
- **Orchestrator Agent**: Coordinates between agents based on user intent
- **API Service**: FastAPI-based API for accessing agent functionality
- **Streamlit UI**: Interactive UI for direct agent interaction

## Installation

### Prerequisites

- Python 3.13.3
- Poetry (for dependency management)

### Using Poetry (Recommended)

This package uses Poetry for dependency management. To install:

```bash
# Install Poetry if you don't have it
curl -sSL https://install.python-poetry.org | python3 -

# Install the package and all dependencies
poetry install

# For development dependencies
poetry install --with dev

# With UI components
poetry install --with ui
```

### Using Docker

```bash
# Build and start the agents using Docker
docker-compose up -d
```

This will start:
- Financial Agents API on port 8000
- Streamlit UI on port 8501

## Usage

### Python API

```python
from financial_agents.orchestrator_agent import app as orchestrator_app

# Process a user query
result = orchestrator_app.invoke({"user_query": "What is a Health Savings Account?"})
print(result["final_response"])
```

### REST API

Access the API at http://localhost:8000

```bash
# Example query using curl
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is a Health Savings Account?"}'
```

### Running the UI

From the package root directory:

```bash
# Run the Streamlit UI
poetry run streamlit run src/ui/app.py
```

Or using Docker:

```bash
# Access the Streamlit UI
open http://localhost:8501
```

## Development

### Project Structure

- `src/` - Source code for the financial agents system
  - `__init__.py`: Package initialization
  - `knowledge_agent.py`: Knowledge agent for financial information
  - `card_agent.py`: Card operations agent
  - `orchestrator_agent.py`: Main orchestrator agent
  - `data/`: Data resources for the agents
  - `ui/`: User interface components
    - `app.py`: Streamlit UI application
    - `api.py`: FastAPI service for web integration
  - `vector_db/`: Vector database for semantic search
  - `scripts/`: Utility scripts

### Docker Support

The repository includes Docker configuration for containerized deployment:

- `Dockerfile`: Python-based image for the agents and API service (Python 3.13.3)
- `docker-compose.yml`: Multi-container setup for the agents, API, and Streamlit UI

## Integration

This package integrates with:

- **Financial Web UI**: React-based frontend (in `../ui-service`)
- **Card API Service**: Java-based API for card operations (in `../card-api-service`)
