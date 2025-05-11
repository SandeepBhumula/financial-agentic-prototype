#!/bin/bash
set -e

# Colors for better output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Financial Agents Service - All-In-One${NC}"
echo -e "${GREEN}===================================${NC}"

# Enable BuildKit for faster, parallel builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

# Default configuration
BUILD_ARGS=""
CLEAN=false
BUILD_ONLY=false
LOGS=false
DETACHED=true
HELP=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --clean)
      CLEAN=true
      BUILD_ARGS="--no-cache"
      shift
      ;;
    --build-only)
      BUILD_ONLY=true
      shift
      ;;
    --logs|-l)
      LOGS=true
      DETACHED=false
      shift
      ;;
    --help|-h)
      HELP=true
      shift
      ;;
    *)
      echo -e "${YELLOW}Warning: Unknown option $1${NC}"
      shift
      ;;
  esac
done

# Show help
if [ "$HELP" = true ]; then
  echo -e "${BLUE}Usage:${NC}"
  echo "  ./start.sh [options]"
  echo ""
  echo -e "${BLUE}Options:${NC}"
  echo "  --clean       Perform a clean build (stop containers, remove volumes, use --no-cache)"
  echo "  --build-only  Only build the images, don't start containers"
  echo "  --logs, -l    Start in foreground mode and show logs"
  echo "  --help, -h    Show this help message"
  echo ""
  echo -e "${BLUE}Examples:${NC}"
  echo "  ./start.sh               # Normal start with caching"
  echo "  ./start.sh --clean       # Clean build and start"
  echo "  ./start.sh --logs        # Start and show logs"
  exit 0
fi

# Stop services if clean build requested
if [ "$CLEAN" = true ]; then
  echo -e "${YELLOW}Performing clean build (stopping containers and using --no-cache)${NC}"
  docker-compose down --remove-orphans
  docker-compose rm -f
fi

# Build images
echo -e "${BLUE}Building Docker images...${NC}"
docker-compose build --parallel $BUILD_ARGS

# Exit if only building
if [ "$BUILD_ONLY" = true ]; then
  echo -e "${GREEN}Build completed successfully!${NC}"
  echo "Run './start.sh' to start the services."
  exit 0
fi

# Start services
if [ "$DETACHED" = true ]; then
  echo -e "${BLUE}Starting services in detached mode...${NC}"
  docker-compose up -d
else
  echo -e "${BLUE}Starting services with logs...${NC}"
  docker-compose up
  # No need to continue the script in this case
  exit 0
fi

# Display running services
echo ""
echo -e "${GREEN}Services started:${NC}"
docker-compose ps

echo ""
echo -e "${GREEN}Access your services at:${NC}"
echo -e "API:      ${BLUE}http://localhost:8000${NC}"
echo -e "UI:       ${BLUE}http://localhost:8501${NC}"
echo -e "ChromaDB: ${BLUE}http://localhost:8100${NC}"
echo ""
echo -e "${YELLOW}Useful commands:${NC}"
echo "  docker-compose logs -f     # View logs"
echo "  docker-compose down        # Stop services"
echo "  ./start.sh --clean         # Rebuild from scratch" 