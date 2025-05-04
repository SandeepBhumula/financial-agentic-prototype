# Financial Agent UI Service

This module provides the web-based user interface for the Financial Agent system, built with React and TypeScript. It connects to the Agents API service and the Card API service to provide a unified interface for users.

## Features

- Dashboard to monitor card metrics and activity
- Card management interface
- Card activation workflow
- Integration with the financial agent system

## Technologies Used

- React 18
- TypeScript
- Material UI
- Docker
- Nginx (for production serving)

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local development)
- Network connectivity to the Agents API and Card API services

## Quick Start

### Using Docker (Recommended)

1. Build the Docker image:
   ```bash
   ./build-ui.sh
   ```

2. Run the service with all required dependencies:
   ```bash
   ./run-ui-service.sh
   ```

3. Access the UI at http://localhost:2025

### Local Development

1. Install dependencies:
   ```bash
   cd web
   npm install --legacy-peer-deps
   ```

2. Start the development server:
   ```bash
   npm start
   ```

3. Access the UI at http://localhost:2025

## Project Structure

```
ui-service/
├── Dockerfile           # Docker configuration for production build
├── docker-compose.yml   # Docker Compose configuration
├── build-ui.sh          # Script to build the Docker image
├── run-ui-service.sh    # Script to run the service with dependencies
├── web/                 # React application
│   ├── public/          # Static assets
│   ├── src/             # Source code
│   ├── package.json     # NPM package configuration
│   ├── tsconfig.json    # TypeScript configuration
│   └── README.md        # React app documentation
└── README.md            # This file
```

## Networking

The UI service connects to the following networks:

- `ui-network` - The network for the UI service
- `agents-network` - For connecting to the Agents API
- `card-api-network` - For connecting to the Card API

The networks are created automatically when running the `run-ui-service.sh` script.

## Accessing the APIs

When running in Docker, the services are available at:

- Agents API: http://agents-api:8000
- Card API: http://card-api:8080

## Troubleshooting

If you encounter issues:

1. Check that all required networks exist:
   ```bash
   docker network ls
   ```

2. Ensure all dependencies are running:
   ```bash
   docker ps
   ```

3. Check the logs:
   ```bash
   docker-compose logs -f
   ```

4. Rebuild the Docker image if needed:
   ```bash
   ./build-ui.sh
   ```
