import os
from typing import TypedDict, Annotated, Sequence
import operator
from langgraph.graph import StateGraph, END
from openai import OpenAI
# from opensearchpy import OpenSearch # Placeholder for actual vector DB client
# Assume vector DB client setup happens elsewhere and is passed or accessed globally/via context

# Environment variable loading
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# --- Agent State ---
class KnowledgeAgentState(TypedDict):
    query: str
    search_results: list[dict] # Results from vector DB
    response: str
    error: str | None

# --- Nodes ---
def retrieve_knowledge(state: KnowledgeAgentState) -> KnowledgeAgentState:
    """Retrieves relevant knowledge from the vector database based on the query."""
    print(f"--- Knowledge Agent: Retrieving knowledge for query: {state['query']} ---")
    query = state['query']
    search_results = []
    error = None
    try:
        # Placeholder: Implement actual vector search logic
        # response = vector_db_client.search(...)
        print("Placeholder: Performing vector search in OpenSearch/Vector DB...")
        # Simulate finding relevant product info from our synthetic data
        if "hsa" in query.lower() or "health savings" in query.lower():
             search_results.append({"id": "HSA001", "text": "Details about Health Savings Account...", "score": 0.9})
        elif "fsa" in query.lower() or "flexible spending" in query.lower():
             search_results.append({"id": "FSA001", "text": "Details about Flexible Spending Account...", "score": 0.88})
        elif "prepaid" in query.lower():
             search_results.append({"id": "PREPAID001", "text": "Details about General Purpose Prepaid Card...", "score": 0.85})
        else:
             search_results.append({"id": "GENERAL", "text": "General financial product information...", "score": 0.7})
        print(f"Found {len(search_results)} potential results.")

    except Exception as e:
        print(f"Error during knowledge retrieval: {e}")
        error = f"Failed to retrieve knowledge: {e}"
        search_results = []

    return {**state, "search_results": search_results, "error": error}

def generate_response(state: KnowledgeAgentState) -> KnowledgeAgentState:
    """Generates a response based on the retrieved knowledge using OpenAI."""
    print("--- Knowledge Agent: Generating response ---")
    if state['error']:
        return {**state, "response": f"Sorry, I encountered an error: {state['error']}"}
    if not state['search_results']:
         return {**state, "response": "I couldn't find specific information for your query."}

    query = state['query']
    context = "\n".join([f"Result {i+1}: {res.get('text', '')} (ID: {res.get('id', 'N/A')})" for i, res in enumerate(state['search_results'])])

    prompt = f"You are a helpful financial knowledge assistant. Answer the user's query based *only* on the provided context.\n\nContext:\n{context}\n\nUser Query: {query}\n\nAnswer:"

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo", # Or specify another model like gpt-4
            messages=[
                {"role": "system", "content": "You are a helpful financial knowledge assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        response = completion.choices[0].message.content
        print(f"Generated response: {response[:100]}...") # Log snippet
    except Exception as e:
        print(f"Error during OpenAI completion: {e}")
        response = f"Sorry, I encountered an error while generating the response: {e}"
        state['error'] = response # Store the error

    return {**state, "response": response}


# --- Graph Definition ---
knowledge_workflow = StateGraph(KnowledgeAgentState)

# Add nodes
knowledge_workflow.add_node("retrieve", retrieve_knowledge)
knowledge_workflow.add_node("generate", generate_response)

# Define edges
knowledge_workflow.set_entry_point("retrieve")
knowledge_workflow.add_edge("retrieve", "generate")
knowledge_workflow.add_edge("generate", END)

# Compile graph
knowledge_agent_app = knowledge_workflow.compile()

# --- Example Usage (for testing) ---
if __name__ == "__main__":
    print("Testing Knowledge Agent...")
    inputs = {"query": "Tell me about health savings accounts"}
    result = knowledge_agent_app.invoke(inputs)
    print("\n--- Final Knowledge Agent Result ---")
    print(result)

    print("\nTesting with a different query...")
    inputs = {"query": "What are the fees for prepaid cards?"}
    result = knowledge_agent_app.invoke(inputs)
    print("\n--- Final Knowledge Agent Result ---")
    print(result) 