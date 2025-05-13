#!/bin/bash

# Installation script for financial-agents service

# Set color codes for better readability
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Detect if we're in a Docker environment
IS_DOCKER=false
if [ -f /.dockerenv ]; then
    IS_DOCKER=true
    echo -e "${YELLOW}Docker environment detected${NC}"
fi

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d " " -f 2)
echo -e "${YELLOW}Using Python version: ${PYTHON_VERSION}${NC}"

# Check if version is 3.9.7 specifically
if [[ "$PYTHON_VERSION" == "3.9.7" ]]; then
    echo -e "${RED}Python 3.9.7 is not compatible with streamlit. Please use a different version.${NC}"
    echo -e "${YELLOW}You can continue, but UI components may not work properly.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Poetry not found, installing...${NC}"
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.2 python3 -
    
    # Add Poetry to PATH for this session
    export PATH="$HOME/.local/bin:$PATH"
fi

# Configure Poetry
echo -e "${YELLOW}Configuring Poetry...${NC}"
if [ "$IS_DOCKER" = true ]; then
    # In Docker, we don't want virtual environments
    poetry config virtualenvs.create false
else
    # Otherwise, create virtual environments in project directory
    poetry config virtualenvs.in-project true
fi

# Create basic directory structure
echo -e "${YELLOW}Creating basic directory structure...${NC}"
mkdir -p notebooks data/chroma_db core ui vector_db tests
touch core/__init__.py ui/__init__.py vector_db/__init__.py tests/__init__.py

# Install the package with Poetry
echo -e "${YELLOW}Installing financial-agents package...${NC}"
# Try with normal install first
if poetry install --with ui --with dev; then
    echo -e "${GREEN}Poetry install succeeded${NC}"
else
    echo -e "${YELLOW}Poetry install failed, trying alternative method...${NC}"
    # If poetry install fails, try with Python environment directly
    echo -e "${YELLOW}Creating Python virtual environment...${NC}"
    
    # Create and activate virtual environment
    python3 -m venv .venv
    source .venv/bin/activate
    
    # Install dependencies directly
    pip install openai langchain langchain-core langchain-openai langgraph python-dotenv pydantic chromadb langchain-chroma
    pip install nbformat jupyter ipykernel
    
    # Register kernel
    python -m ipykernel install --user --name=financial-agents --display-name="Financial Agents Environment"
    
    echo -e "${GREEN}Virtual environment setup complete${NC}"
fi

# Create Jupyter kernel if not in Docker
if [ "$IS_DOCKER" = false ]; then
    echo -e "${YELLOW}Creating Jupyter kernel for project...${NC}"
    poetry run python -m ipykernel install --user --name=financial-agents --display-name="Financial Agents Environment"
fi

# Set up environment variables for Chroma
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file with Chroma DB settings...${NC}"
    cat > .env << EOF
# OpenAI API key - YOU MUST SET THIS
OPENAI_API_KEY=

# Chroma DB settings
CHROMA_PERSIST_DIRECTORY=$(pwd)/data/chroma_db
CHROMA_USE_PERSISTENT=true
# Use the following for server mode if needed
# CHROMA_HOST=localhost
# CHROMA_PORT=8100
# CHROMA_USE_PERSISTENT=false
EOF
    echo -e "${GREEN}Created .env file with Chroma DB settings${NC}"
else
    # Check if Chroma settings exist in .env, if not add them
    if ! grep -q "CHROMA_PERSIST_DIRECTORY" .env; then
        echo -e "${YELLOW}Adding Chroma DB settings to .env file...${NC}"
        cat >> .env << EOF

# Chroma DB settings
CHROMA_PERSIST_DIRECTORY=$(pwd)/data/chroma_db
CHROMA_USE_PERSISTENT=true
# Use the following for server mode if needed
# CHROMA_HOST=localhost
# CHROMA_PORT=8100
# CHROMA_USE_PERSISTENT=false
EOF
        echo -e "${GREEN}Added Chroma DB settings to .env file${NC}"
    fi
fi

# Create the notebook from the Python file
if [ -f merged_agents.py ]; then
    echo -e "${YELLOW}Creating Jupyter notebook from merged_agents.py...${NC}"
    command -v python && python notebook_util.py --input merged_agents.py --output notebooks/merged_financial_agents.ipynb || \
    poetry run python notebook_util.py --input merged_agents.py --output notebooks/merged_financial_agents.ipynb 
    echo -e "${GREEN}Notebook created and fixed${NC}"
fi

# Guide user on how to initialize the vector database
echo -e "${GREEN}Installation complete!${NC}"
echo -e "${YELLOW}To initialize the Chroma vector database, run:${NC}"
echo -e "  poetry run python -m vector_db.run_setup"

# Guide user on how to run the project
echo -e "${YELLOW}To run the notebook:${NC}"
echo -e "  1. Start Jupyter notebook: poetry run jupyter notebook${NC}"
echo -e "  2. Open notebooks/merged_financial_agents.ipynb${NC}"
echo -e "  3. Select kernel 'Financial Agents Environment'${NC}"
echo -e "  4. Add this code to the first cell to fix import issues:${NC}"
echo -e "     import sys, os; sys.path.insert(0, os.path.abspath('..')); print('Path fixed')${NC}"

echo -e "${YELLOW}To run the service with Docker:${NC}"
echo -e "  docker-compose up"

echo -e "${YELLOW}To activate the Poetry environment:${NC}"
echo -e "  poetry shell" 