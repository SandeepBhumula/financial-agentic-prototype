import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import the orchestrator agent from the financial_agents package
try:
    from financial_agents.orchestrator_agent import app as orchestrator_app
    orchestrator_available = True
except ImportError as e:
    print(f"Failed to import orchestrator agent: {e}")
    print("Make sure the financial-agents package is installed")
    orchestrator_available = False
except Exception as e:
    print(f"An unexpected error occurred during agent import: {e}")
    orchestrator_available = False

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

# Request model
class QueryRequest(BaseModel):
    query: str

# Response model
class QueryResponse(BaseModel):
    response: str
    success: bool
    error: str = None

@app.get("/")
async def root():
    return {"status": "online", "orchestrator_available": orchestrator_available}

@app.post("/api/chat", response_model=QueryResponse)
async def chat(request: QueryRequest):
    if not orchestrator_available:
        raise HTTPException(status_code=503, detail="Orchestrator agent is not available")
    
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

# Run the API server if this file is executed directly
if __name__ == "__main__":
    # Run the API server on port 8000
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True) 