# Financial Agents Service

This service provides conversational AI agents for financial services, including:

- Knowledge Agent: Answers questions about financial products
- Card Agent: Handles card-related actions like activation and deactivation
- Orchestrator Agent: Coordinates between other agents based on user intent

## Getting Started

### Local Development

```bash
# Install dependencies
poetry install

# Run API
uvicorn ui.api:app --reload
```

### Docker Development

```bash
# Build and run with Docker Compose
docker-compose up -d
```

## Configuration

Set environment variables in `.env` file:

```
OPENAI_API_KEY=your_api_key
```

## Features

- **Knowledge Agent**: Retrieves information about financial products from a vector database
- **Card Agent**: Executes card-related actions (activate, deactivate)
- **Orchestrator Agent**: Coordinates between agents based on user intent

## Installation

### Prerequisites

- Docker and Docker Compose (required)
- Python 3.9 or higher (optional, for local development only)
- [Poetry](https://python-poetry.org/docs/#installation) (optional, for local development only)

### Quick Install

Run the installer script:

```bash
./install.sh
```

This will:
- Verify Docker and Docker Compose are installed
- Create necessary environment files and directories
- Make all scripts executable
- Guide you through adding your OpenAI API key
- Provide instructions on how to start the services

After installation, simply run:

```bash
./start.sh
```

All services will be built and started automatically.

### Manual Installation

If you prefer to install manually:

1. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Configure Poetry:
   ```bash
   poetry config virtualenvs.in-project true
   ```

3. Install the project dependencies:
   ```bash
   poetry install --with ui --with dev
   ```

4. Create a `.env` file based on `.env.example`:
   ```bash
   cp .env.example .env
   ```
   
5. Edit the `.env` file and add your OpenAI API key.

6. Register the Jupyter kernel:
   ```bash
   poetry run python -m ipykernel install --user --name=financial-agents --display-name="Financial Agents Environment"
   ```

## Running the Project

### Running with Poetry (Local Development)

1. Activate the Poetry shell:
   ```bash
   poetry shell
   ```

2. Initialize the vector database:
   ```bash
   python -m vector_db.run_setup
   ```

3. Run the FastAPI server:
   ```bash
   uvicorn ui.api:app --host 0.0.0.0 --port 8000 --reload
   ```

4. In a separate terminal, run the Streamlit UI:
   ```bash
   streamlit run ui/app.py
   ```

### Running with Docker

The easiest way to build and run all services is to use our all-in-one script:

```bash
# Build and start all services
./start.sh

# For a clean build (removes existing containers)
./start.sh --clean

# To only build the containers without starting
./start.sh --build-only

# To see all logs in real-time
./start.sh --logs

# To see all available options
./start.sh --help
```

This will start:
- The FastAPI server at http://localhost:8000
- The Streamlit UI at http://localhost:8501 
- The Jupyter Notebook environment at http://localhost:8888
- The ChromaDB service at http://localhost:8100

The vector database is automatically initialized when the containers start up. This behavior can be controlled with the `INITIALIZE_VECTOR_DB` environment variable in the docker-compose.yml file.

For detailed information about the Docker build optimizations and advanced configuration options, please see [DOCKER.md](DOCKER.md).

**Note:** You can still use the individual commands if preferred:
```bash
# Build only
./build.sh

# Start services
docker-compose up -d
```

### Running Jupyter Notebooks

To run the notebooks:

1. With Poetry (local):
   ```bash
   poetry run jupyter notebook notebooks/merged_financial_agents.ipynb
   ```
   
   Make sure to select the "Financial Agents Environment" kernel.

2. With Docker:
   - Start the services: `docker-compose up`
   - Access Jupyter at http://localhost:8888
   - Navigate to the `notebooks` folder

## Project Structure

```
financial-agents-service/
├── core/                 # Core business logic
├── data/                 # Data files and vector database storage
│   └── chroma_db/        # Persistent storage for ChromaDB
├── financial_agents/     # Main package for import
├── notebooks/            # Jupyter notebooks for exploration and testing
│   └── merged_financial_agents.ipynb  # Combined agents notebook
├── tests/                # Test suite
├── ui/                   # User interfaces (API and Streamlit)
├── vector_db/            # Vector database setup and utilities
├── Dockerfile            # Docker container definition
├── docker-compose.yml    # Multi-container Docker setup
├── pyproject.toml        # Poetry configuration and dependencies
└── install.sh            # Installation script
```

## Development

### Adding New Dependencies

To add new dependencies:

```bash
poetry add package-name
```

For development dependencies:

```bash
poetry add package-name --group dev
```

For UI dependencies:

```bash
poetry add package-name --group ui
```

### Running Tests

```bash
poetry run pytest
```

## License

[License information]
