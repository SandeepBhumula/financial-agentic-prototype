"""
Financial Agents System - Merged Implementation

This file combines three financial agent components into a single integrated system:

1. Knowledge Agent: Retrieves information about financial products
2. Card Agent: Executes card-related actions (activate, deactivate)
3. Orchestrator Agent: Coordinates between the other agents based on user intent

Each component is fully defined with its own state types, functions, and graph workflow.
"""

import os
import json
import logging
import requests
from typing import TypedDict, Annotated, Sequence, Dict, Any, List, Optional, Literal
from pathlib import Path
import operator

from langgraph.graph import StateGraph, END
from openai import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
import pandas as pd
import chromadb

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Environment variable loading
from dotenv import load_dotenv
load_dotenv()

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CHROMA_HOST = os.environ.get("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.environ.get("CHROMA_PORT", "8000"))
CHROMA_PERSIST_DIRECTORY = os.environ.get("CHROMA_PERSIST_DIRECTORY", 
                                         os.path.join(Path(__file__).parent, "data", "chroma_db"))
USE_PERSISTENT = os.environ.get("CHROMA_USE_PERSISTENT", "true").lower() == "true"
COLLECTION_NAME = "healthcare_financial_data"

EMBEDDING_MODEL = "text-embedding-3-large"
LLM_MODEL = "gpt-4-turbo"
DATA_DIR = os.path.join(Path(__file__).parent, 'data')

# Card API configuration
CARD_API_BASE_URL = "http://card-api:8080/api/cards"  # Using Docker service name

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

#################################################
# Knowledge Agent Implementation
#################################################

# --- Knowledge Agent State ---
class KnowledgeAgentState(TypedDict):
    query: str
    search_results: List[Dict[str, Any]]
    response: str
    error: Optional[str]
    account_types: List[str]
    intent: Optional[str]

# --- Vector DB Setup ---
def load_data_for_vectorization():
    """
    Load financial and healthcare data for vector db ingestion
    """
    data_sources = []
    
    # Load accounts data
    accounts_file = os.path.join(DATA_DIR, 'synthetic_healthcare_accounts.csv')
    if os.path.exists(accounts_file):
        logger.info(f"Loading accounts data from {accounts_file}")
        try:
            accounts_df = pd.read_csv(accounts_file)
            accounts_text = accounts_df.to_csv(index=False)
            data_sources.append({
                "content": accounts_text,
                "metadata": {"source": "healthcare_accounts"}
            })
        except Exception as e:
            logger.error(f"Failed to load accounts data: {e}")
    
    # Load transactions data
    transactions_file = os.path.join(DATA_DIR, 'synthetic_healthcare_transactions.csv')
    if os.path.exists(transactions_file):
        logger.info(f"Loading transactions data from {transactions_file}")
        try:
            transactions_df = pd.read_csv(transactions_file)
            # Take a sample if it's too large
            if len(transactions_df) > 10000:
                transactions_df = transactions_df.sample(10000)
            transactions_text = transactions_df.to_csv(index=False)
            data_sources.append({
                "content": transactions_text,
                "metadata": {"source": "healthcare_transactions"}
            })
        except Exception as e:
            logger.error(f"Failed to load transactions data: {e}")
    
    # Load product data
    products_file = os.path.join(DATA_DIR, 'synthetic_healthcare_products.json')
    if os.path.exists(products_file):
        logger.info(f"Loading products data from {products_file}")
        try:
            with open(products_file, 'r') as f:
                products_data = json.load(f)
                # Process each product separately for better chunks
                for product in products_data.get("products", []):
                    product_text = json.dumps(product, indent=2)
                    data_sources.append({
                        "content": product_text,
                        "metadata": {
                            "source": "healthcare_products",
                            "product_id": product.get("id", ""),
                            "product_name": product.get("name", "")
                        }
                    })
        except Exception as e:
            logger.error(f"Failed to load products data: {e}")
    
    # Load plans data
    plans_file = os.path.join(DATA_DIR, 'synthetic_healthcare_plans.json')
    if os.path.exists(plans_file):
        logger.info(f"Loading plans data from {plans_file}")
        try:
            with open(plans_file, 'r') as f:
                plans_data = json.load(f)
                plans_text = json.dumps(plans_data, indent=2)
                data_sources.append({
                    "content": plans_text,
                    "metadata": {"source": "healthcare_plans"}
                })
        except Exception as e:
            logger.error(f"Failed to load plans data: {e}")
    
    return data_sources

def create_chunks(data_sources):
    """
    Create optimally sized chunks from the data sources
    """
    # Constants from the instruction prompt
    CHUNK_SIZE = 600
    CHUNK_OVERLAP = 90  # 15% of chunk size
    
    logger.info(f"Creating chunks with size={CHUNK_SIZE}, overlap={CHUNK_OVERLAP}")
    
    # Initialize the text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        add_start_index=True
    )
    
    all_chunks = []
    
    # Process each data source
    for source in data_sources:
        content = source["content"]
        metadata = source["metadata"]
        
        # Split the text into chunks
        texts = text_splitter.split_text(content)
        
        # Create documents for each chunk
        for i, text in enumerate(texts):
            # Enrich metadata with chunk information
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_id"] = i
            chunk_metadata["chunk_count"] = len(texts)
            
            all_chunks.append({"text": text, "metadata": chunk_metadata})
    
    logger.info(f"Created {len(all_chunks)} chunks from {len(data_sources)} data sources")
    return all_chunks

def get_embedding_client():
    """
    Get the OpenAI embeddings client
    """
    try:
        embeddings = OpenAIEmbeddings(
            model=EMBEDDING_MODEL,
            openai_api_key=OPENAI_API_KEY
        )
        return embeddings
    except Exception as e:
        logger.error(f"Failed to initialize embeddings client: {e}")
        return None

def get_vector_store():
    """
    Get or create the ChromaDB vector store with our healthcare financial data
    """
    # Check if we have a flag file indicating the vector store has been populated
    flag_file = os.path.join(DATA_DIR, 'vector_store_populated.flag')
    
    # Get embeddings client
    embeddings = get_embedding_client()
    if not embeddings:
        logger.error("Cannot get vector store - embeddings client initialization failed")
        return None
    
    # Initialize the vector store
    try:
        # Set the appropriate implementation based on environment
        if USE_PERSISTENT:
            # For local persistent mode
            logger.info(f"Initializing local ChromaDB at {CHROMA_PERSIST_DIRECTORY}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                persist_directory=CHROMA_PERSIST_DIRECTORY
            )
        else:
            # For server/containerized mode using REST API
            logger.info(f"Initializing ChromaDB with REST API at {CHROMA_HOST}:{CHROMA_PORT}")
            vector_store = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=embeddings,
                client_settings=chromadb.config.Settings(
                    chroma_api_impl="rest",
                    chroma_server_host=CHROMA_HOST,
                    chroma_server_http_port=CHROMA_PORT,
                    anonymized_telemetry=False
                )
            )
        
        # If flag exists, return the existing vector store
        if os.path.exists(flag_file):
            logger.info("Using existing vector store")
            return vector_store
        
        # Otherwise, populate the vector store
        logger.info("Populating vector store with healthcare financial data")
        
        # Load and chunk data
        data_sources = load_data_for_vectorization()
        chunks = create_chunks(data_sources)
        
        # Populate vector store with chunks
        for chunk in chunks:
            vector_store.add_texts(
                texts=[chunk["text"]],
                metadatas=[chunk["metadata"]]
            )
        
        # Persist if using persistent mode
        if USE_PERSISTENT:
            vector_store.persist()
        
        # Create flag file
        with open(flag_file, 'w') as f:
            f.write("Vector store populated on " + pd.Timestamp.now().isoformat())
        
        logger.info(f"Vector store populated with {len(chunks)} chunks")
        return vector_store
    
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        return None

# --- Knowledge Agent Node Functions ---
def retrieve_knowledge(state: KnowledgeAgentState) -> KnowledgeAgentState:
    """Retrieves relevant knowledge from the vector database based on the query."""
    logger.info(f"Retrieving knowledge for query: {state['query']}")
    query = state['query']
    search_results = []
    error = None
    
    # Identify account types mentioned in the query
    account_types = []
    for account_type in ["HSA", "FSA", "Health Savings Account", "Flexible Spending Account", 
                       "Dependent Care", "Prepaid", "Health Care Spend"]:
        if account_type.lower() in query.lower():
            short_type = account_type
            if account_type == "Health Savings Account":
                short_type = "HSA"
            elif account_type == "Flexible Spending Account":
                short_type = "FSA"
            
            if short_type not in account_types:
                account_types.append(short_type)
    
    # Get vector store
    vector_store = get_vector_store()
    
    try:
        if vector_store:
            # Enhance query with account types if specified
            enhanced_query = query
            if account_types:
                account_types_str = ", ".join(account_types)
                enhanced_query = f"{query} relevant to {account_types_str}"
            
            # Perform vector search
            docs = vector_store.similarity_search(enhanced_query, k=5)
            
            # Process search results
            for doc in docs:
                search_results.append({
                    "text": doc.page_content,
                    "source": doc.metadata.get("source", "unknown"),
                    "product_id": doc.metadata.get("product_id", ""),
                    "product_name": doc.metadata.get("product_name", "")
                })
            
            logger.info(f"Found {len(search_results)} search results")
        else:
            # Fallback to mock data if vector store is not available
            logger.warning("Vector store not available. Using mock data.")
            
            # Mock results based on query
            if "hsa" in query.lower() or "health savings" in query.lower():
                search_results.append({
                    "text": "Health Savings Account (HSA) is a tax-advantaged savings account for individuals with high-deductible health plans. The 2024 contribution limit for individuals is $4,150 and for families is $8,300.",
                    "source": "healthcare_products",
                    "product_id": "HSA001",
                    "product_name": "Health Savings Account (HSA)"
                })
            elif "fsa" in query.lower() or "flexible spending" in query.lower():
                search_results.append({
                    "text": "Flexible Spending Account (FSA) is an employer-sponsored account allowing employees to set aside pre-tax dollars for eligible healthcare expenses. The 2024 contribution limit is $3,200.",
                    "source": "healthcare_products",
                    "product_id": "FSA001",
                    "product_name": "Flexible Spending Account (FSA)"
                })
            else:
                search_results.append({
                    "text": "Healthcare financial products include HSAs, FSAs, Dependent Care accounts, and Prepaid cards. Each has different eligibility requirements and benefits.",
                    "source": "healthcare_products",
                    "product_id": "",
                    "product_name": ""
                })
    except Exception as e:
        logger.error(f"Error during knowledge retrieval: {e}")
        error = f"Failed to retrieve knowledge: {e}"
        search_results = []
    
    # Classify query intent
    intent = classify_intent(query)
    
    return {
        **state, 
        "search_results": search_results, 
        "error": error,
        "account_types": account_types,
        "intent": intent
    }

def classify_intent(query: str) -> str:
    """Classify the intent of the query."""
    try:
        # Use OpenAI to classify intent
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": """You are an intent classifier for healthcare financial queries.
                    Classify the user's intent into one of these categories:
                    - INFORMATION: General question about healthcare financial products
                    - COMPARISON: Comparing different healthcare account types
                    - ELIGIBILITY: Questions about eligibility for specific accounts
                    - CONTRIBUTION: Questions about contribution limits or rules
                    - SPENDING: Questions about spending rules or eligible expenses
                    - OTHER: Any other intent
                    
                    Return ONLY the intent category, nothing else."""},
                {"role": "user", "content": query}
            ],
            temperature=0.1
        )
        
        intent = completion.choices[0].message.content.strip()
        
        # Normalize the intent
        for valid_intent in ["INFORMATION", "COMPARISON", "ELIGIBILITY", "CONTRIBUTION", "SPENDING", "OTHER"]:
            if valid_intent in intent:
                return valid_intent
        
        return "OTHER"
    except Exception as e:
        logger.error(f"Error classifying intent: {e}")
        return "OTHER"

def generate_response(state: KnowledgeAgentState) -> KnowledgeAgentState:
    """Generates a response based on the retrieved knowledge using OpenAI."""
    logger.info("Generating response")
    
    if state['error']:
        return {**state, "response": f"Sorry, I encountered an error: {state['error']}"}
    
    if not state['search_results']:
        return {**state, "response": "I couldn't find specific information for your query."}
    
    query = state['query']
    account_types = state.get('account_types', [])
    intent = state.get('intent', 'OTHER')
    
    # Construct context from search results
    context_parts = []
    for i, result in enumerate(state['search_results']):
        source_info = f" (Source: {result['source']})"
        if result['product_name']:
            source_info += f" (Product: {result['product_name']})"
        
        context_parts.append(f"Result {i+1}: {result['text']}{source_info}")
    
    context = "\n\n".join(context_parts)
    
    # Prepare prompt for response generation
    prompt_template = """You are a healthcare financial expert assistant. 
    Answer the following question based on the context provided.
    
    Context:
    {context}
    
    User's question: {query}
    
    Account types mentioned: {account_types}
    Intent: {intent}
    
    Give a clear, concise, and accurate answer based on the context. If the context doesn't contain the answer, 
    acknowledge that you don't have enough information rather than making up an answer.
    Focus on providing factual information relevant to healthcare financial accounts.
    """
    
    try:
        # Generate response
        completion = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": prompt_template.format(
                    context=context,
                    query=query,
                    account_types=", ".join(account_types) if account_types else "None specifically mentioned",
                    intent=intent
                )},
                {"role": "user", "content": query}
            ],
            temperature=0.2
        )
        
        response = completion.choices[0].message.content
        logger.info(f"Generated response: {response[:100]}...")
    except Exception as e:
        logger.error(f"Error during OpenAI completion: {e}")
        response = f"Sorry, I encountered an error while generating the response: {e}"
        state['error'] = str(e)  # Store the error
    
    return {**state, "response": response}

# --- Knowledge Agent Graph Definition ---
knowledge_workflow = StateGraph(KnowledgeAgentState)

# Add nodes
knowledge_workflow.add_node("retrieve", retrieve_knowledge)
knowledge_workflow.add_node("generate", generate_response)

# Define edges
knowledge_workflow.set_entry_point("retrieve")
knowledge_workflow.add_edge("retrieve", "generate")
knowledge_workflow.add_edge("generate", END)

# Compile graph
knowledge_agent = knowledge_workflow.compile()

def handle_query(query: str) -> str:
    """Handle a user query and return a response."""
    initial_state = {
        "query": query,
        "search_results": [],
        "response": "",
        "error": None,
        "account_types": [],
        "intent": None
    }
    
    try:
        result = knowledge_agent.invoke(initial_state)
        return result["response"]
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return f"An error occurred while processing your query: {str(e)}"


#################################################
# Card Agent Implementation
#################################################

# --- Card Agent State ---
class CardAgentState(TypedDict):
    action: str # e.g., "activate", "deactivate"
    card_number: str # The last four digits of the card
    parameters: dict # Any additional parameters needed for the API call
    api_response: dict | None # Response from the card API
    confirmation_message: str # User-facing message
    error: str | None

# --- Card Agent Tool (API Call Function) ---
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

# --- Card Agent Nodes ---
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

# --- Card Agent Graph Definition ---
card_workflow = StateGraph(CardAgentState)

# Add node
card_workflow.add_node("execute", execute_card_action)

# Define edges
card_workflow.set_entry_point("execute")
card_workflow.add_edge("execute", END)

# Compile graph
card_agent_app = card_workflow.compile()


#################################################
# Orchestrator Agent Implementation
#################################################

# --- Orchestrator State ---
class OrchestratorState(TypedDict):
    user_query: str
    intent: Literal["knowledge", "card_action", "unknown", "error"]
    card_action_details: CardAgentState | None # Details needed for card agent
    knowledge_agent_response: str | None
    card_agent_response: str | None
    final_response: str
    error: str | None

# --- Orchestrator Nodes ---
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

# --- Orchestrator Conditional Edges ---
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

# --- Orchestrator Graph Definition ---
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
orchestrator_app = workflow.compile()


#################################################
# Testing Functions
#################################################

def test_knowledge_agent(query: str):
    """Test the knowledge agent with a query."""
    print(f"\n--- Testing Knowledge Agent with query: {query} ---")
    
    initial_state = {
        "query": query,
        "search_results": [],
        "response": "",
        "error": None,
        "account_types": [],
        "intent": None
    }
    
    try:
        result = knowledge_agent.invoke(initial_state)
        print("\n--- Knowledge Agent Result ---")
        print(f"Response: {result['response']}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return {"response": f"Error: {e}", "error": str(e)}

def test_card_agent(action: str, card_number: str, parameters: dict = None):
    """Test the card agent with specified action and parameters."""
    if parameters is None:
        parameters = {}
    
    print(f"\n--- Testing Card Agent: {action} for card {card_number} ---")
    
    initial_state = {
        "action": action,
        "card_number": card_number,
        "parameters": parameters,
        "api_response": None,
        "confirmation_message": "",
        "error": None
    }
    
    try:
        result = card_agent_app.invoke(initial_state)
        print("\n--- Card Agent Result ---")
        print(f"Confirmation: {result.get('confirmation_message')}")
        if result.get('error'):
            print(f"Error: {result.get('error')}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return {"confirmation_message": f"Error: {e}", "error": str(e)}

def test_orchestrator(query: str):
    """Test the orchestrator with a user query."""
    print(f"\n--- Testing Orchestrator with query: {query} ---")
    
    initial_state = {
        "user_query": query,
        "intent": "unknown",
        "card_action_details": None,
        "knowledge_agent_response": None,
        "card_agent_response": None,
        "final_response": "",
        "error": None
    }
    
    try:
        result = orchestrator_app.invoke(initial_state)
        print("\n--- Orchestrator Result ---")
        print(f"Intent: {result['intent']}")
        print(f"Final Response: {result['final_response']}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        return {"final_response": f"Error: {e}", "error": str(e)}


#################################################
# Example Usage
#################################################

if __name__ == "__main__":
    print("\n=====================================")
    print("FINANCIAL AGENTS SYSTEM - MERGED DEMO")
    print("=====================================\n")
    
    # Test Knowledge Agent
    print("\n----- KNOWLEDGE AGENT DEMO -----\n")
    knowledge_queries = [
        "What is an HSA account?",
        "What's the contribution limit for FSA in 2024?",
        "How do prepaid healthcare cards work?"
    ]
    
    for query in knowledge_queries:
        test_knowledge_agent(query)
    
    # Test Card Agent
    print("\n----- CARD AGENT DEMO -----\n")
    test_card_agent("activate", "1234", {"cvv": "123", "expiryDate": "12/25"})
    test_card_agent("deactivate", "5678", {"reason": "Lost card"})
    
    # Test Orchestrator
    print("\n----- ORCHESTRATOR DEMO -----\n")
    orchestrator_queries = [
        "What are the benefits of an HSA account?",
        "Activate my card ending in 1234 with CVV 123",
        "What's the weather today?"
    ]
    
    for query in orchestrator_queries:
        test_orchestrator(query) 