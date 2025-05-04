# Financial Agent UI

This is a React-based frontend for the Financial Agent service, providing a modern and user-friendly interface for interacting with various financial services.

## Features

- **Dashboard**: View account balances, recent transactions, and spending trends
- **Card Management**: View and manage your cards, including locking/unlocking features
- **Card Activation**: Step-by-step process for activating new cards
- **Chat Assistant**: AI-powered chat interface for customer support and inquiries

## Getting Started

### Prerequisites

- Node.js 14 or higher
- npm or yarn

### Installation

1. Clone the repository
2. Navigate to the project directory
3. Install dependencies:

```bash
npm install
```

### Running the App

Start the development server:

```bash
npm start
```

The app will be available at [http://localhost:2025](http://localhost:2025).

### Integration with Backend Services

The UI is designed to connect to the Financial Agent backend services, including:

- LangGraph Orchestrator Agent 
- Card Agent
- Knowledge Agent

By default, it uses mock data for demonstration purposes. To connect to actual backend services, update the API endpoints in the respective service files.

## Project Structure

- `/src/components`: Reusable UI components
- `/src/pages`: Main application pages
- `/src/services`: API and service integrations
- `/src/utils`: Utility functions and helpers

## Technologies Used

- React
- TypeScript
- Material-UI
- React Router
- Chart.js

## License

This project is licensed under the MIT License.
