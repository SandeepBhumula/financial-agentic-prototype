import os
import sys
import requests
from typing import Dict, Any, Optional

# Add the parent directory to the path to enable absolute imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)  # Path to 'agents' directory
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Direct import using absolute imports
from fastapi import FastAPI, HTTPException, Request, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

# Create FastAPI app
app = FastAPI(title="Financial Agent API")

# Add CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, set this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Import other modules after the app is initialized
# This ensures the health endpoint is available even if there are import errors
try:
    # Direct import using absolute path - this avoids relative import issues
    from core.orchestrator import app as orchestrator_app
    from core.card import card_agent_app
except Exception as e:
    print(f"Warning: Error importing modules: {e}")
    # We'll still allow the API to start for health checks

# Request models
class QueryRequest(BaseModel):
    query: str

class CardRequest(BaseModel):
    operation: str
    payload: Dict[str, Any]

# Response models
class QueryResponse(BaseModel):
    response: str
    success: bool
    error: Optional[str] = None

class CardOperationResponse(BaseModel):
    success: bool
    message: str
    cardNumber: str = "****"
    data: Optional[Dict[str, Any]] = None

# API endpoints
@app.get("/")
async def root():
    return {"status": "online"}

@app.post("/api/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    try:
        # Invoke the orchestrator agent
        inputs = {"user_query": request.query}
        result = orchestrator_app.invoke(inputs)
        response = result.get('final_response', "Sorry, I could not process your request.")
        
        return {
            "response": response,
            "success": True
        }
    except Exception as e:
        return {
            "response": "An error occurred while processing your request.",
            "success": False,
            "error": str(e)
        }

# Single card operation endpoint that works with the card agent
@app.post("/api/cards/operation", response_model=CardOperationResponse)
async def card_operation(request: CardRequest):
    try:
        # Extract operation and parameters
        operation = request.operation
        payload = request.payload
        
        # Prepare state for card agent
        state = {
            "action": operation,
            "card_number": payload.get("cardLastFour") or payload.get("cardNumber", ""),
            "parameters": payload,
            "api_response": None,
            "confirmation_message": "",
            "error": None
        }
        
        # Invoke card agent
        result = card_agent_app.invoke(state)
        
        # Format response
        card_number = state["card_number"]
        if len(card_number) > 4:
            card_number = card_number[-4:].rjust(16, '*')
        
        return {
            "success": result.get("error") is None,
            "message": result.get("confirmation_message", "Operation completed"),
            "cardNumber": card_number,
            "data": result.get("api_response")
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Error processing card operation: {str(e)}",
            "cardNumber": "****"
        }

# Run the API server if this file is executed directly
if __name__ == "__main__":
    # Run the API server on port 8000
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 