#!/bin/bash

# Define terminal colors for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to display help information
show_help() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Financial Package Management Script${NC}"
  echo -e "${BLUE}=====================================${NC}"
  echo -e "Usage: ./run.sh [command]"
  echo -e ""
  echo -e "Commands:"
  echo -e "  ${GREEN}start${NC}      - Start all services"
  echo -e "  ${GREEN}stop${NC}       - Stop all services"
  echo -e "  ${GREEN}restart${NC}    - Restart all services"
  echo -e "  ${GREEN}status${NC}     - Check status of services"
  echo -e "  ${GREEN}logs${NC}       - Show logs from all services"
  echo -e "  ${GREEN}logs [service]${NC} - Show logs for a specific service"
  echo -e "  ${GREEN}clean${NC}      - Remove all containers, networks, and volumes"
  echo -e "  ${GREEN}help${NC}       - Show this help message"
  echo -e ""
  echo -e "Services:"
  echo -e "  ${BLUE}web-ui${NC}      - Web UI (port 2025)"
  echo -e "  ${BLUE}agents-api${NC}  - Agents API (port 8000)"
  echo -e "  ${BLUE}card-api${NC}    - Card API (port 8080)"
  echo -e "  ${BLUE}postgres${NC}    - PostgreSQL Database (port 5432)"
  echo -e ""
}

# Function to start all services
start_services() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Starting Financial Package Stack${NC}"
  echo -e "${BLUE}=====================================${NC}"

  # Check if Docker is running
  if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
  fi

  # Start all services
  echo -e "${YELLOW}Starting all services...${NC}"
  docker-compose -f docker-compose.yml up -d

  # Wait for services to be healthy
  echo -e "${YELLOW}Waiting for services to be healthy...${NC}"
  sleep 5

  echo -e "${GREEN}All services are now running!${NC}"
  echo -e "${BLUE}You can access the services at:${NC}"
  echo -e "Web UI: http://localhost:2025"
  echo -e "API Service: http://localhost:8000"
  echo -e "Card API Service: http://localhost:8080"
}

# Function to stop all services
stop_services() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Stopping Financial Package Stack${NC}"
  echo -e "${BLUE}=====================================${NC}"

  echo -e "${YELLOW}Stopping all services...${NC}"
  docker-compose -f docker-compose.yml down

  echo -e "${GREEN}All services stopped${NC}"
}

# Function to restart all services
restart_services() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Restarting Financial Package Stack${NC}"
  echo -e "${BLUE}=====================================${NC}"

  stop_services
  start_services
}

# Function to check status of services
check_status() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Financial Package Stack Status${NC}"
  echo -e "${BLUE}=====================================${NC}"

  docker-compose -f docker-compose.yml ps
}

# Function to show logs
show_logs() {
  if [ -z "$1" ]; then
    echo -e "${BLUE}=====================================${NC}"
    echo -e "${YELLOW}Financial Package Stack Logs${NC}"
    echo -e "${BLUE}=====================================${NC}"
    
    echo -e "${YELLOW}Showing logs for all services...${NC}"
    docker-compose -f docker-compose.yml logs -f
  else
    echo -e "${BLUE}=====================================${NC}"
    echo -e "${YELLOW}Logs for $1${NC}"
    echo -e "${BLUE}=====================================${NC}"
    
    echo -e "${YELLOW}Showing logs for $1...${NC}"
    docker-compose -f docker-compose.yml logs -f "$1"
  fi
}

# Function to clean up all resources
clean_resources() {
  echo -e "${BLUE}=====================================${NC}"
  echo -e "${YELLOW}Cleaning Financial Package Stack${NC}"
  echo -e "${BLUE}=====================================${NC}"

  echo -e "${YELLOW}Stopping all services...${NC}"
  docker-compose -f docker-compose.yml down -v

  echo -e "${YELLOW}Removing all containers, networks, and volumes...${NC}"
  docker-compose -f docker-compose.yml rm -f

  echo -e "${GREEN}All resources cleaned${NC}"
}

# Main script logic
case "$1" in
  start)
    start_services
    ;;
  stop)
    stop_services
    ;;
  restart)
    restart_services
    ;;
  status)
    check_status
    ;;
  logs)
    show_logs "$2"
    ;;
  clean)
    clean_resources
    ;;
  help|--help|-h|"")
    show_help
    ;;
  *)
    echo -e "${RED}Unknown command: $1${NC}"
    show_help
    exit 1
    ;;
esac 