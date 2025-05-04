# Financial Agentic Prototype

This project is a microservices-based financial system with AI-powered agents that help users manage their finances. It implements a multi-agent system for handling financial card services and knowledge retrieval.

## Architecture

The system consists of three main services:

1. **financial-card-service**: Java/Spring Boot service for managing payment cards and transactions
2. **financial-agents-service**: Python-based AI service using LLMs for financial assistance
3. **financial-ui-service**: Web-based user interface

## Project Structure

```
.
├── financial-package/                      # Main project package
│   ├── financial-agents-service/           # Python agent implementations (LangGraph, OpenAI)
│   │   ├── __init__.py
│   │   ├── card_agent.py
│   │   ├── knowledge_agent.py
│   │   └── orchestrator_agent.py
│   ├── financial-card-service/             # Java Spring Boot API for card actions
│   │   ├── pom.xml
│   │   └── src/
│   │       ├── main/
│   │       │   ├── java/com/financialagent/cardapi/
│   │       │   │   ├── CardApiApplication.java
│   │       │   │   ├── controllers/       # API endpoints
│   │       │   │   │   └── CardController.java
│   │       │   │   └── dtos/              # Data Transfer Objects
│   │       │   │       ├── ActivateCardRequest.java
│   │       │   │       ├── CardActionRequest.java
│   │       │   │       ├── CardActionResponse.java
│   │       │   │       └── DeactivateCardRequest.java
│   │       │   └── resources/
│   │       │       └── application.properties # Spring Boot configuration
│   │       └── test/                      # (Placeholder for Java tests)
│   ├── financial-ui-service/              # User Interface with React
│   │   ├── web/                           # Web UI with React
│   │   │   ├── src/
│   │   │   │   ├── components/            # UI components
│   │   │   │   ├── pages/                 # UI pages including Dashboard
│   │   │   │   └── services/              # API service connectors
│   │   └── api/                           # Backend for UI
├── financial-requirements/                # Requirements and documentation
│   ├── CapStone project.rtf               # Original project description
│   └── UI Screen template.pdf             # UI design templates
├── requirements.txt                       # Python dependencies
└── README.md                              # This file
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- OpenAI API key for the agents service
- Python 3.8+ for development
- Java/Maven for card service development
- Node.js for UI development

### Running the System with Docker

To run the entire system:

```bash
cd financial-package
docker-compose up -d
```

To run individual services:

```bash
# For card service only
cd financial-package/financial-card-service
docker-compose up -d

# For agents service (includes card service)
cd financial-package/financial-agents-service
docker-compose up -d

# For UI service (includes all services)
cd financial-package/financial-ui-service
docker-compose up -d
```

### Accessing Services

- Card API: http://localhost:8080
- Agents API: http://localhost:8000
- Agents UI: http://localhost:8501
- Web UI: http://localhost:2025

## Setup for Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd financial_agentic_prototype
   ```

2. **Python Environment:**
   * Create and activate a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate # On Windows use `venv\Scripts\activate`
     ```
   * Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```
   * **API Keys:** Create a `.env` file in the project root and add your OpenAI API key:
     ```
     OPENAI_API_KEY="your_openai_api_key_here"
     ```

3. **Java Card API Service:**
   * Navigate to the API directory:
     ```bash
     cd financial-package/financial-card-service
     ```
   * Build and run the Spring Boot application:
     ```bash
     ./mvnw spring-boot:run # Use mvnw.cmd on Windows
     ```
   * The API will be available at `http://localhost:8080/api/cards`.

4. **Run the UI Service:**
   * Navigate to the UI directory:
     ```bash
     cd financial-package/financial-ui-service/web
     ```
   * Install dependencies:
     ```bash
     npm install
     ```
   * Start the development server:
     ```bash
     npm start
     ```
   * The UI will be available at `http://localhost:3000`.

## Features

### Dashboard UI
* Financial account balances including HSA, FSA, prepaid card, and healthcare spending
* Transaction history from various accounts including healthcare spending
* Spending categories visualization with healthcare spending breakdown
* Spending trend analysis
* Interactive agent chat for financial assistance

### Healthcare Account Management 
* Health Savings Account (HSA): Tax-advantaged medical savings
* Flexible Spending Account (FSA): Pre-tax account for healthcare expenses
* Prepaid Healthcare Cards: Direct payment for medical expenses
* Healthcare Spending Tracking: Monitor and analyze healthcare expenses

### Card Management
* Activate and deactivate cards
* View card details
* Manage card settings

### Agent System Components
* **Card Agent**: Handles card operations (activation/deactivation)
* **Knowledge Agent**: Provides information about financial products and services
* **Orchestrator Agent**: Routes user queries to the appropriate specialized agent

## Debug Tools

### Agent Debugging Interface

For debugging the agent system, you can use the included notebook:

1. Start Jupyter: `jupyter notebook`
2. Open `agent_debug_notebook.ipynb`
3. Configure your environment and API keys
4. Run the cells to test agents individually or the full orchestration

## Troubleshooting

* **OpenAI API Errors**: Verify your API key is valid and has sufficient quota
* **Card API Connection Errors**: Ensure the Java Card API service is running
* **Docker Issues**: Use `docker-compose logs` to view service logs
* **Network Problems**: Check that all required ports are available 