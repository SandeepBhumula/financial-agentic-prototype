# Card API Service

Java-based API for card operations in the Financial Agents system.

## Features

- REST API for card management operations
- Activation, deactivation, and status check for financial cards
- PostgreSQL database for persistent storage
- Spring Boot backend with Flyway migrations

## Getting Started

### Using Docker (Recommended)

```bash
# Start the service with Docker Compose
docker-compose up -d
```

This will start:
- PostgreSQL database on port 5432
- Card API service on port 8080

### Manual Installation

Prerequisites:
- Java 17 or higher
- Maven 3.6 or higher
- PostgreSQL 14

```bash
# Build with Maven
mvn clean package

# Run the application
java -jar target/card-api-0.0.1-SNAPSHOT.jar
```

## API Endpoints

- **GET /api/cards**: List all cards
- **GET /api/cards/{id}**: Get card details
- **POST /api/cards**: Create a new card
- **PUT /api/cards/{id}/activate**: Activate a card
- **PUT /api/cards/{id}/deactivate**: Deactivate a card

## Docker Support

The repository includes Docker configuration for containerized deployment:

- `Dockerfile`: Java-based image for the Card API service
- `docker-compose.yml`: Multi-container setup with PostgreSQL database

## Integration

This service integrates with the Financial Agents system and is used by:

- **Financial Agents**: AI agents for financial services (in `../agents`)
- **Web UI**: Frontend for user interaction (in `../ui-service`)
