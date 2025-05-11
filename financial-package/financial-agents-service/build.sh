#!/bin/bash
set -e

echo "Optimized Docker build script"
echo "============================="

# Enable BuildKit for faster, parallel builds
export DOCKER_BUILDKIT=1
export COMPOSE_DOCKER_CLI_BUILD=1

BUILD_ARGS=""

# Handle script arguments
if [ "$1" == "--clean" ]; then
  echo "Performing clean build (removing existing containers and using --no-cache)"
  docker-compose down --remove-orphans
  docker-compose rm -f
  BUILD_ARGS="--no-cache"
fi

# Build images with optimizations
echo "Building Docker images with optimizations..."
docker-compose build --parallel $BUILD_ARGS

echo "Build completed successfully!"
echo "You can now run 'docker-compose up -d' to start the services." 