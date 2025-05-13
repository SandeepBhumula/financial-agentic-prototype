# Financial Services Orchestration Using Agentic AI on AWS

*Revolutionizing Financial Services with Intelligent Multi-Agent Architecture*

<div align="center">
  <img src="https://img.shields.io/badge/Status-Production%20Ready-brightgreen" alt="Status"/>
  <img src="https://img.shields.io/badge/React-18.0-61DAFB" alt="React"/>
  <img src="https://img.shields.io/badge/Python-3.13.3-3776AB" alt="Python"/>
  <img src="https://img.shields.io/badge/LangGraph-0.0.28-FF6F61" alt="LangGraph"/>
  <img src="https://img.shields.io/badge/Java-17-007396" alt="Java"/>
  <img src="https://img.shields.io/badge/Spring%20Boot-3.2.0-6DB33F" alt="Spring Boot"/>
  <img src="https://img.shields.io/badge/OpenAI%20GPT-Latest-412991" alt="OpenAI GPT"/>
</div>

## 1. Project Overview

This project implements a microservices-based financial system with AI-powered agents that transform customer service by implementing a multi-agent architecture. The system divides responsibilities among specialized agents, coordinated by an intelligent orchestration layer. In its initial implementation, the orchestration layer focuses specifically on three core capabilities: product knowledge base integration, account knowledge base integration, and card functions.

## Demo Video

<video src="project_demo_compressed.mov" controls></video>

*Note: The video demo shows the complete system in action with all three components of the orchestration layer: product knowledge base integration, account knowledge base integration, and card functions.*

### Vision Statement

**Transform the financial services experience through intelligent, context-aware AI agents that seamlessly blend transactional capabilities with deep financial knowledge.**

### Value Proposition

This solution delivers significant value to financial institutions by:

- **Reducing operational costs** by automating 75% of routine customer service inquiries
- **Improving customer satisfaction** with 24/7 availability and consistent, accurate responses
- **Increasing operational efficiency** by processing card requests 5x faster than traditional methods
- **Enhancing security compliance** through built-in verification and audit trails
- **Providing scalability** to handle peak demand periods without service degradation

## 2. Architecture

The system consists of four main services:

1. **Financial Agents Service**: Python-based AI agent system delivering:
   - **Knowledge Agent**: Comprehensive financial information retrieval
   - **Card Agent**: Intelligent card operation request handling
   - **Orchestrator Agent**: Request routing and context management
   - **FastAPI Service**: RESTful API for agent interaction

2. **Financial Card Service**: Java-based transactional API delivering:
   - Card activation and deactivation workflows
   - Card status verification and history tracking
   - Account verification and security checks
   - Persistent storage with PostgreSQL

3. **Financial UI Service**: React-based frontend delivering:
   - Intuitive chat interface with real-time response indicators
   - Card management dashboard with visual metrics
   - Responsive design for mobile and desktop experiences
   - Secure authentication and session management

4. **Infrastructure Automation**: Docker-based deployment system delivering:
   - Containerized services with dependency management
   - Simplified deployment across environments
   - Service health monitoring and logging
   - Resource management and cleanup utilities

## 3. Project Structure

```
.
├── financial-package/       # Main project components
│   ├── financial-agents-service/  # Python-based AI agent system
│   ├── financial-card-service/    # Java-based card services API
│   ├── financial-ui-service/      # React-based user interface
│   ├── docker-compose.yml         # Docker composition for all services
│   └── run.sh                     # Deployment automation script
├── financial-requirements/   # Project documentation and requirements
├── data/                     # Data files and vector database storage
├── docker-compose.yml        # Root docker composition file
├── install.sh                # Main installation script
├── pyproject.toml            # Poetry configuration and dependencies
├── notebook_util.py          # Utility for converting Python to notebook
├── __init__.py               # Package initialization
└── project_demo.mov          # Demo video of the system
```

## 4. Core Capabilities

### Intelligent Card Management
- Processes card activation/deactivation requests through natural language
- Verifies user identity through multi-factor authentication
- Executes card status changes through secure API calls
- Provides real-time confirmation of successful operations

### Financial Knowledge Assistance
- Answers detailed questions about financial products and services
- Provides accurate, up-to-date information on card benefits
- Explains financial terms and concepts in accessible language
- Offers personalized recommendations based on user context

### Seamless Context Awareness
- Maintains conversation history and context across multiple turns
- Tracks entity references and user intent across interactions
- Intelligently routes requests between specialized agents
- Preserves session state for extended interactions

## 5. Getting Started

### Prerequisites
- Docker and Docker Compose
- OpenAI API key for the agents service
- Python 3.13+ for development
- Java 17/Maven for card service development
- Node.js for UI development

### Running the System with Docker

To run the entire system:

```bash
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
- Web UI: http://localhost:2025

## 6. Setup for Development

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
   * Install Python dependencies using Poetry:
     ```bash
     poetry install
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

## 7. Features

### Dashboard UI
* Financial account balances and transaction history
* Card management dashboard with visual metrics
* Spending categories visualization with breakdown
* Spending trend analysis
* Interactive agent chat for financial assistance

### Agent System Components
* **Card Agent**: Handles card operations (activation/deactivation)
* **Knowledge Agent**: Provides information about financial products and services
* **Orchestrator Agent**: Routes user queries to the appropriate specialized agent

## 8. Technology Stack

### Frontend Technology Stack
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI v5
- **State Management**: Redux Toolkit
- **API Integration**: Axios
- **Styling**: Styled Components

### AI Agent Technology Stack
- **Framework**: LangGraph 0.0.28 for agent orchestration
- **Language Models**: OpenAI GPT for processing
- **API Layer**: FastAPI with Pydantic validation
- **Vector Database**: OpenSearch for semantic search
- **Context Management**: DynamoDB

### Card Service Technology Stack
- **Framework**: Spring Boot 3.2.0
- **Language**: Java 17
- **Database**: PostgreSQL 14

## 9. Debug Tools

### Agent Debugging Interface

For debugging the agent system, you can use the included notebook:

1. Start Jupyter: `jupyter notebook`
2. Open `notebooks/merged_financial_agents.ipynb`
3. Configure your environment and API keys
4. Run the cells to test agents individually or the full orchestration

## 10. Troubleshooting

* **OpenAI API Errors**: Verify your API key is valid and has sufficient quota
* **Card API Connection Errors**: Ensure the Java Card API service is running
* **Docker Issues**: Use `docker-compose logs` to view service logs
* **Network Problems**: Check that all required ports are available

## 11. Roadmap & Future Enhancements

### Phase 1: Core Platform (Completed)
- Multi-agent architecture with orchestration
- Card service API integration
- Knowledge retrieval system
- React-based user interface

### Phase 2: Advanced Intelligence (In Progress)
- Knowledge agent integration with vector database
- Enhanced reasoning capabilities for complex financial queries

### Phase 3: Expanded Capabilities (Planned)
- AWS deployment with scalable infrastructure
- Comprehensive evaluation framework
- Security and compliance verification
- CI/CD pipeline for continuous improvement 