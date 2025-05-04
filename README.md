# Financial Card Services Agentic AI Prototype

This project implements a multi-agent system for handling financial card services and knowledge retrieval, based on the concepts outlined in the Capstone project proposal.

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

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd financial_agentic_prototype
    ```

2.  **Python Environment:**
    *   Create and activate a virtual environment (recommended):
        ```bash
        python -m venv venv
        source venv/bin/activate # On Windows use `venv\Scripts\activate`
        ```
    *   Install Python dependencies:
        ```bash
        pip install -r requirements.txt
        ```
    *   **API Keys:** Create a `.env` file in the project root and add your OpenAI API key:
        ```
        OPENAI_API_KEY="your_openai_api_key_here"
        ```
        Update the agent files (`financial-package/financial-agents-service/*.py`) to load the key from the environment variable using `python-dotenv` instead of hardcoding it.

3.  **Java Card API Service:**
    *   Navigate to the API directory:
        ```bash
        cd financial-package/financial-card-service
        ```
    *   Build and run the Spring Boot application using Maven:
        ```bash
        ./mvnw spring-boot:run # Use mvnw.cmd on Windows
        ```
    *   The API stub will be available at `http://localhost:8080/api/cards`.
    *   To implement database interactions:
        *   Uncomment the JPA and SQL Server dependencies in `pom.xml`.
        *   Configure your SQL Server connection details in `src/main/resources/application.properties`.
        *   Implement JPA entities, repositories, and service logic to replace the placeholder comments in `CardController.java`.

4.  **Run the UI Service:**
    *   Navigate to the UI directory:
        ```bash
        cd financial-package/financial-ui-service/web
        ```
    *   Install dependencies:
        ```bash
        npm install
        ```
    *   Start the development server:
        ```bash
        npm start
        ```
    *   The UI will be available at `http://localhost:3000`.

5. **Run All Services Together:**
    * Use the provided script:
        ```bash
        ./financial-package/run.sh start
        ```
    * This script will start all necessary services (UI, Card API, and Agent services).

## Features

### Dashboard UI

The dashboard includes:
* Financial account balances including HSA, FSA, prepaid card, and healthcare spending
* Transaction history from various accounts including healthcare spending
* Spending categories visualization with healthcare spending breakdown
* Spending trend analysis
* Interactive agent chat for financial assistance

### Healthcare Account Management 

The system supports management of various healthcare spending accounts:
* Health Savings Account (HSA): Tax-advantaged medical savings
* Flexible Spending Account (FSA): Pre-tax account for healthcare expenses
* Prepaid Healthcare Cards: Direct payment for medical expenses
* Healthcare Spending Tracking: Monitor and analyze healthcare expenses

### Card Management

* Activate and deactivate cards
* View card details
* Manage card settings

### Knowledge Agent

* Ask questions about financial products and services
* Get information about healthcare spending accounts
* Receive assistance with financial decisions

## Usage

*   Interact with the dashboard to view financial and healthcare information.
*   Use the chat interface to ask questions about financial products and services.
*   Manage cards through the card management interface.
*   View and analyze transactions across different account types.

# Financial Agent System Debugger

This repository contains a debugging interface for a multi-agent financial system with the following components:

- **Card Agent**: Handles card operations (activation/deactivation)
- **Knowledge Agent**: Provides information about financial products and services
- **Orchestrator Agent**: Routes user queries to the appropriate specialized agent

## Getting Started

### Prerequisites

Before running the notebook, ensure you have the following:

1. Python 3.8+ installed
2. Jupyter notebook or JupyterLab installed
3. Required Python packages (install with `pip install -r requirements.txt`):
   - langgraph
   - openai
   - requests
   - python-dotenv
   - jupyter
   - ipywidgets

### OpenAI API Key

You'll need a valid OpenAI API key to use the agents. You can:
- Set it as an environment variable: `export OPENAI_API_KEY=your_key_here`
- Update it directly in the notebook configuration cell

### Card API Service

The Card Agent interacts with a Java-based card service API. For complete testing:
1. Ensure the card service is running at `http://localhost:8080/api/cards`
2. If not running, the Card Agent will simulate calls but return connection errors

## Using the Notebook

1. Start Jupyter:
   ```
   jupyter notebook
   ```

2. Open `agent_debug_notebook.ipynb`

3. Run the cells in sequence, following the numbered sections:
   - Configure your environment and API keys
   - Import the agents
   - Test each agent individually
   - Test the orchestration workflow
   - Use the interactive demo

4. Debug Mode Options:
   - Enable debug mode in the relevant sections to see detailed internal states
   - Use the API connection tests to verify connectivity
   - Test intent classification with custom queries

## Notebook Sections

1. **Setup & Configuration**: Environment setup and API key configuration
2. **Import Agents**: Loading the three agent systems
3. **Helper Functions**: Utilities for formatting and tracing
4. **Card Agent Debug**: Test card operations directly
5. **Knowledge Agent Debug**: Test financial knowledge queries
6. **Orchestrator Debug**: Test the complete system with intent classification
7. **Interactive Demo**: Conversational UI for testing
8. **System Diagnostics**: API and connectivity tests
9. **Custom Testing**: Advanced debugging for specific components

## Troubleshooting

- **OpenAI API Errors**: Verify your API key is valid and has sufficient quota
- **Card API Connection Errors**: Ensure the Java Card API service is running
- **Import Errors**: Make sure you've installed all required packages
- **Widget Display Issues**: Install/enable the Jupyter widgets extension if needed 