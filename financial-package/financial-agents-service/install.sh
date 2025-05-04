#!/bin/bash

# Installation script for financial-agents package

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

# Check if Poetry is installed
if ! command -v poetry &> /dev/null; then
    echo -e "${YELLOW}Poetry not found, installing...${NC}"
    curl -sSL https://install.python-poetry.org | POETRY_VERSION=2.1.2 python3 -
fi

# Configure Poetry
echo -e "${YELLOW}Configuring Poetry...${NC}"
poetry config virtualenvs.create false

# Install the package
echo -e "${YELLOW}Installing financial-agents package...${NC}"
poetry install --with ui

# If in Docker, create compatibility symlinks
if [ "$IS_DOCKER" = true ]; then
    echo -e "${YELLOW}Creating compatibility links for Docker...${NC}"
    
    # Create a symlink for backward compatibility if not exists
    if [ ! -d "financial_agents" ] && [ -d "src" ]; then
        ln -sf "$(pwd)/src" "$(pwd)/financial_agents"
        echo -e "${GREEN}Created symlink from src to financial_agents${NC}"
    fi
    
    # Add current directory to PYTHONPATH in .bashrc or similar
    if [ -f ~/.bashrc ]; then
        grep -qxF 'export PYTHONPATH=$PYTHONPATH:$(pwd)' ~/.bashrc || echo 'export PYTHONPATH=$PYTHONPATH:$(pwd)' >> ~/.bashrc
        echo -e "${GREEN}Added current directory to PYTHONPATH in .bashrc${NC}"
    fi
fi

echo -e "${GREEN}Installation complete!${NC}"
echo -e "You can now import the package as: ${YELLOW}from financial_agents import ...${NC}" 