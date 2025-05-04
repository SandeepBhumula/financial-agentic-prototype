import os
import requests
from typing import TypedDict
from langgraph.graph import StateGraph, END
from openai import OpenAI
from dotenv import load_dotenv

# Environment variable loading
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Configuration ---
# Base URL for the Card Service API (adjust as needed)
CARD_API_BASE_URL = "http://card-api:8080/api/cards" # Updated to use the Docker service name

# --- Agent State ---
class CardAgentState(TypedDict):
    action: str # e.g., "activate", "deactivate"
    card_number: str # The last four digits of the card
    parameters: dict # Any additional parameters needed for the API call
    api_response: dict | None # Response from the card API
    confirmation_message: str # User-facing message
    error: str | None

# --- Tool (API Call Function) ---
def call_card_api(action: str, card_number: str, parameters: dict) -> dict:
    """Calls the Card Service API."""
    url = f"{CARD_API_BASE_URL}/{action}"
    payload = {"cardLastFour": card_number, **parameters}
    
    try:
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'}, timeout=10)
        api_data = response.json() if response.content else {"message": "No content"}
        
        if response.ok:
            return {"success": True, **api_data}
        
        return {
            "success": False,
            "message": api_data.get("message", f"Error {response.status_code}"),
            "status_code": response.status_code,
            "api_response": api_data
        }
    except Exception as e:
        return {"success": False, "message": f"API error: {str(e)}"}

# --- Nodes ---
def execute_card_action(state: CardAgentState) -> CardAgentState:
    """Executes the requested card action by calling the API."""
    api_result = call_card_api(state['action'], state['card_number'], state['parameters'])
    
    if api_result.get("success"):
        confirmation_message = api_result.get("message", f"Card {state['action']} processed successfully.")
    else:
        confirmation_message = f"Failed to {state['action']} card. Error: {api_result.get('message')}"
    
    return {
        **state, 
        "api_response": api_result, 
        "confirmation_message": confirmation_message, 
        "error": None if api_result.get("success") else api_result.get("message")
    }

# --- Graph Definition ---
card_workflow = StateGraph(CardAgentState)

# Add node
card_workflow.add_node("execute", execute_card_action)

# Define edges
card_workflow.set_entry_point("execute")
card_workflow.add_edge("execute", END)

# Compile graph
card_agent_app = card_workflow.compile() 