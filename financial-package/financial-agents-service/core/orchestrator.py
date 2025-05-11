import os
from typing import TypedDict, Annotated, Sequence, Literal
import operator
from langgraph.graph import StateGraph, END
from openai import OpenAI

# Import agent apps (assuming they are runnable)
from core.knowledge import knowledge_agent, KnowledgeAgentState # Use relative import
from core.card import card_agent_app, CardAgentState # Use relative import

# Environment variable loading
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Orchestrator State ---
class OrchestratorState(TypedDict):
    user_query: str
    intent: Literal["knowledge", "card_action", "unknown", "error"]
    card_action_details: CardAgentState | None # Details needed for card agent
    knowledge_agent_response: str | None
    card_agent_response: str | None
    final_response: str
    error: str | None

# --- Nodes ---
def classify_intent(state: OrchestratorState) -> OrchestratorState:
    """Classifies the user's intent using OpenAI."""
    print(f"--- Orchestrator: Classifying intent for query: {state['user_query']} ---")
    query = state['user_query']
    intent = "unknown"
    error = None
    card_action_details = None
    
    # Initialize response fields to None
    knowledge_agent_response = None
    card_agent_response = None

    prompt = f"""Classify the user's intent based on their query. Choose one: 'knowledge', 'card_action', or 'unknown'.
    - 'knowledge': User is asking for information (e.g., 'What is an HSA?', 'Tell me about prepaid cards').
    - 'card_action': User wants to perform an action on a card (e.g., 'Activate my card', 'Deactivate card ending in 1234').
    - 'unknown': The intent is unclear or not related to finance/cards.

    If the intent is 'card_action', extract the following information in JSON format:
    - "intent": "card_action"
    - "action": The action to perform (e.g., "activate", "deactivate")
    - "card_identifier": Card number or last 4 digits
    - "parameters": A dictionary of additional parameters like:
        - "cvv": Card CVV (if provided)
        - "expiryDate": Card expiry date in format MM/YY (if provided)
        - "reason": Reason for deactivation (if provided)
    
    For example, if the user says "I want to activate my card ending in 4444 with CVV 123 and expiry date 05/26",
    you should return:
    {{"intent": "card_action", "action": "activate", "card_identifier": "4444", "parameters": {{"cvv": "123", "expiryDate": "05/26"}}}}
    
    If the intent is 'knowledge' or 'unknown', format as JSON: {{"intent": "..."}}

    User Query: "{query}"

    JSON Output:"""

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Use a model suitable for classification
            messages=[
                {"role": "system", "content": "You are an intent classification expert for financial services."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"} # Request JSON output if model supports
        )
        result_json = json.loads(completion.choices[0].message.content)
        intent = result_json.get("intent", "unknown")
        print(f"Classified intent: {intent}")

        if intent == "card_action":
            action = result_json.get("action")
            card_identifier = result_json.get("card_identifier")
            parameters = result_json.get("parameters", {})
            
            # Print the extracted parameters for debugging
            print(f"Extracted parameters: {parameters}")
            
            if action and card_identifier:
                # In a real system, you'd need more robust extraction and potentially clarification
                card_action_details = {
                    "action": action,
                    "card_number": card_identifier, # May need validation/lookup
                    "parameters": parameters, # Now properly extracting and using parameters
                    # Initialize other CardAgentState fields as None or empty
                    "api_response": None,
                    "confirmation_message": "",
                    "error": None
                }
                print(f"Extracted card action details: {card_action_details}")
            else:
                print("Warning: card_action intent detected but details missing.")
                intent = "unknown" # Fallback if details can't be extracted
                error = "Could not extract necessary details for the card action."

    except Exception as e:
        print(f"Error during intent classification: {e}")
        intent = "error"
        error = f"Failed to classify intent: {e}"

    # Return a properly initialized state with all fields
    return {
        **state,
        "intent": intent,
        "card_action_details": card_action_details,
        "knowledge_agent_response": knowledge_agent_response,
        "card_agent_response": card_agent_response,
        "error": error
    }

def route_to_knowledge_agent(state: OrchestratorState) -> OrchestratorState:
    """Invokes the Knowledge Agent."""
    print("--- Orchestrator: Routing to Knowledge Agent ---")
    try:
        response = handle_query(state['user_query'])
        error = None
        print(f"Knowledge Agent Result: {response[:100]}...")
    except Exception as e:
        response = "Knowledge agent did not provide a response."
        error = str(e)
        print(f"Knowledge Agent Error: {error}")
    
    return {**state, "knowledge_agent_response": response, "error": error}

def route_to_card_agent(state: OrchestratorState) -> OrchestratorState:
    """Invokes the Card Agent."""
    print("--- Orchestrator: Routing to Card Agent ---")
    if not state['card_action_details']:
        error = "Cannot route to card agent: missing action details."
        print(error)
        return {**state, "card_agent_response": "Internal error: Missing card action details.", "error": error}

    card_input = state['card_action_details']
    card_result = card_agent_app.invoke(card_input) # Invoke with the prepared CardAgentState
    response = card_result.get("confirmation_message", "Card agent did not provide a response.")
    error = card_result.get("error")
    print(f"Card Agent Result: {response[:100]}... Error: {error}")
    return {**state, "card_agent_response": response, "error": error}

def format_final_response(state: OrchestratorState) -> OrchestratorState:
    """Formats the final response based on which agent was called."""
    print("--- Orchestrator: Formatting final response ---")
    
    # Handle error condition
    if state.get('error'):
        if state['intent'] == 'card_action' and state.get('card_agent_response'):
            # Use the card agent response directly if it exists
            final_response = state['card_agent_response']
        elif state['intent'] == 'knowledge' and state.get('knowledge_agent_response'):
            # Use the knowledge agent response directly if it exists
            final_response = state['knowledge_agent_response']
        else:
            # Generic error response if no agent-specific response is available
            final_response = f"Sorry, I encountered an error processing your request: {state['error']}"
    # Handle successful responses
    elif state['intent'] == 'knowledge':
        final_response = state.get('knowledge_agent_response', "I couldn't retrieve the information.")
    elif state['intent'] == 'card_action':
        final_response = state.get('card_agent_response', "The card action request could not be completed.")
    else:
        final_response = "I'm not sure how to handle that request. Can you please rephrase?"

    print(f"Final Response: {final_response[:100]}...")
    return {**state, "final_response": final_response}

# --- Conditional Edges ---
def decide_route(state: OrchestratorState) -> Literal["knowledge", "card_action", "end_error", "end_unknown"]:
    """Determines the next step based on the classified intent."""
    print(f"--- Orchestrator: Deciding route based on intent: {state['intent']} ---")
    if state.get('error') and state['intent'] == 'error':
        return "end_error"
    elif state['intent'] == 'knowledge':
        return "knowledge"
    elif state['intent'] == 'card_action':
        if state['card_action_details']: # Check if details were extracted
             return "card_action"
        else:
             print("Routing to end_unknown due to missing card details despite intent.")
             return "end_unknown" # Treat as unknown if details missing
    else: # unknown
        return "end_unknown"

# Import the handle_query function from knowledge
from core.knowledge import handle_query

# --- Graph Definition ---
import json # Need json for the classifier node
workflow = StateGraph(OrchestratorState)

# Add nodes
workflow.add_node("classify_intent", classify_intent)
workflow.add_node("knowledge_agent", route_to_knowledge_agent)
workflow.add_node("card_agent", route_to_card_agent)
workflow.add_node("format_response", format_final_response)

# Define edges
workflow.set_entry_point("classify_intent")

# Conditional routing after classification
workflow.add_conditional_edges(
    "classify_intent",
    decide_route,
    {
        "knowledge": "knowledge_agent",
        "card_action": "card_agent",
        "end_error": "format_response", # Go directly to formatting for critical errors
        "end_unknown": "format_response" # Go directly to formatting for unknown intent
    }
)

# Edges from agents to final formatting
workflow.add_edge("knowledge_agent", "format_response")
workflow.add_edge("card_agent", "format_response")

# End after formatting
workflow.add_edge("format_response", END)

# Compile graph
app = workflow.compile()

# --- Example Usage (for testing) ---
if __name__ == "__main__":
    print("\n--- Testing Orchestrator (Knowledge Intent) ---")
    inputs_knowledge = {"user_query": "What are the benefits of an FSA?"}
    result_knowledge = app.invoke(inputs_knowledge)
    print("\n--- Final Orchestrator Result (Knowledge) ---")
    print(result_knowledge.get('final_response'))

    print("\n--- Testing Orchestrator (Card Action Intent) ---")
    inputs_card = {"user_query": "Please activate my card ending in 4444 with CVV 123 and expiry date 05/26"}
    result_card = app.invoke(inputs_card)
    print("\n--- Final Orchestrator Result (Card Action) ---")
    print(result_card.get('final_response'))

    print("\n--- Testing Orchestrator (Unknown Intent) ---")
    inputs_unknown = {"user_query": "What is the weather today?"}
    result_unknown = app.invoke(inputs_unknown)
    print("\n--- Final Orchestrator Result (Unknown) ---")
    print(result_unknown.get('final_response')) 