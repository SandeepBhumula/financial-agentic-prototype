# Financial Agents Package

This is a comprehensive package for financial services AI agents with containerized deployment support.

## Project Structure

- **agents/** - LangGraph-based financial AI agents and API service (Python 3.13.3)
  - Knowledge Agent - Provides financial product knowledge
  - Card Agent - Handles card actions (activation, deactivation, etc.)
  - Orchestrator Agent - Main entry point that routes queries to specialized agents
  - FastAPI Service - API for interacting with agents

- **card-api-service/** - API service for card-related operations
  - Java-based card management API

- **ui-service/** - React-based frontend
  - Web UI - Modern React application for financial services

## Getting Started

### Prerequisites

- Docker and Docker Compose v2.20.0 or newer (required for composition using include directive)
- (Optional) Python 3.13.3 for local development
- (Optional) Node.js 16+ for local frontend development
- (Optional) Java 17+ for local card API development

### Using Docker (Recommended)

You can run the entire stack using a single command:

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=your-api-key-here

# Start all services
docker compose up -d
```

This will start:
- Financial Agents API on port 8000
- Streamlit UI on port 8501 
- Web UI on port 3000
- Card API on port 8080
- PostgreSQL database for card service

### Individual Components

Each component has been designed to automatically include its dependencies:

```bash
# Run the agents (automatically includes the card API service)
cd agents
docker compose up -d
```

```bash
# Run the web UI (automatically includes agents and card API)
cd ui-service
docker compose up -d
```

```bash
# Run just the card API service
cd card-api-service
docker compose up -d
```

### Component Dependencies

The system uses Docker Compose's include feature to manage dependencies between components:

- **card-api-service**: Standalone service with PostgreSQL database
- **agents**: Depends on card-api-service
- **ui-service**: Depends on both agents and card-api-service 
- **Root docker-compose.yml**: Includes all three services

This modular approach allows you to run any component and have its dependencies automatically started.

## Accessing the Services

- **Web UI**: http://localhost:2025
- **Streamlit UI**: http://localhost:8501
- **Agents API**: http://localhost:8000
- **Card API**: http://localhost:8080

## Architecture

```
           ┌─────────────┐
           │   Web UI    │
           │  (React)    │
           └──────┬──────┘
                  │
                  ▼
┌─────────────────────────────────┐
│        Financial Agents         │
│   ┌───────────┐                 │
│   │ Streamlit │                 │
│   │    UI     │                 │
│   └─────┬─────┘                 │
│         │                       │
│         ▼                       │
│   ┌───────────┐    ┌───────────┐│     ┌───────────────┐
│   │ FastAPI   │    │LangGraph  ││     │ Card API      │
│   │ Service   │───▶│ Agents    │├────▶│ (Java)        │
│   └───────────┘    └───────────┘│     └───────┬───────┘
└─────────────────────────────────┘             │
                                                ▼
                                         ┌─────────────┐
                                         │ PostgreSQL  │
                                         │ Database    │
                                         └─────────────┘
```

## License

MIT 