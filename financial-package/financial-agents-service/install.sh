#!/bin/bash

# Financial Agents Service Installer
# This script will set up everything you need to run the Financial Agents Service

# Exit on error
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=========================================${NC}"
echo -e "${BLUE}   Financial Agents Service Installer    ${NC}"
echo -e "${BLUE}=========================================${NC}"

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo -e "${YELLOW}Docker is not installed. Please install Docker first: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${YELLOW}Docker Compose is not installed. Please install Docker Compose first: https://docs.docker.com/compose/install/${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env 2>/dev/null || echo "OPENAI_API_KEY=" > .env
    echo -e "${GREEN}Created .env file. Please edit it to add your OpenAI API key.${NC}"
    echo -e "${YELLOW}Please edit the .env file now to add your OpenAI API key.${NC}"
    sleep 2
    
    # Open .env file with default editor if possible
    if command -v nano &> /dev/null; then
        nano .env
    elif command -v vim &> /dev/null; then
        vim .env
    elif command -v vi &> /dev/null; then
        vi .env
    else
        echo -e "${YELLOW}Please manually edit the .env file to add your OPENAI_API_KEY.${NC}"
    fi
fi

# Make scripts executable
echo -e "${YELLOW}Making scripts executable...${NC}"
chmod +x start.sh build.sh docker-entrypoint.sh 2>/dev/null || true
echo -e "${GREEN}Scripts are now executable.${NC}"

# Create data directories if they don't exist
echo -e "${YELLOW}Creating data directories...${NC}"
mkdir -p data/chroma_db
echo -e "${GREEN}Data directories created.${NC}"

echo -e "${BLUE}=========================================${NC}"
echo -e "${GREEN}Installation complete!${NC}"
echo -e "${BLUE}=========================================${NC}"
echo
echo -e "To start the Financial Agents Service, run: ${YELLOW}./start.sh${NC}"
echo -e "For a clean build: ${YELLOW}./start.sh --clean${NC}"
echo -e "For more options: ${YELLOW}./start.sh --help${NC}"
echo
echo -e "${BLUE}Available services when running:${NC}"
echo -e "- API: ${YELLOW}http://localhost:8000${NC}"
echo -e "- UI: ${YELLOW}http://localhost:8501${NC}"
echo -e "- Jupyter: ${YELLOW}http://localhost:8888${NC}"
echo -e "- ChromaDB: ${YELLOW}http://localhost:8100${NC}"
echo 