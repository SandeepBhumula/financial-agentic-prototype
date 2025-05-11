#!/usr/bin/env python3
"""
Notebook Utility

A consolidated script to handle conversion of Python files to Jupyter notebooks
and fixing any compatibility issues.

Usage:
    python notebook_util.py [--input merged_agents.py] [--output notebooks/merged_financial_agents.ipynb]
"""

import os
import re
import sys
import json
import logging
import argparse
from pathlib import Path
import nbformat as nbf

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_docstring(content):
    """Extract the docstring from the Python file."""
    docstring_match = re.match(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        return docstring_match.group(1).strip(), content[docstring_match.end():]
    return None, content

def find_section_headers(content):
    """Find section headers in the Python file."""
    # Match section headers like "# --- Section Name ---" or "#################################################"
    # or "# Section Name"
    section_patterns = [
        r'#\s*---\s*(.*?)\s*---\s*#*',  # Match "# --- Section Name ---"
        r'#\s*(.*?)\s*Implementation\s*#*',  # Match "# Knowledge Agent Implementation ###"
        r'#\s*(.*?)\s*State\s*#*',  # Match "# Knowledge Agent State ###"
        r'#\s*(.*?)\s*#+'  # For headers surrounded by hashes
    ]
    
    sections = []
    for pattern in section_patterns:
        for match in re.finditer(pattern, content):
            section_title = match.group(1).strip()
            if section_title and not (section_title.startswith("---") or len(section_title) < 3):
                # Skip separator lines and very short titles
                sections.append((match.start(), section_title))
    
    # Additional patterns for imports and main block
    if "import " in content:
        import_match = re.search(r'import\s+', content)
        if import_match:
            sections.append((import_match.start(), "Imports and Configuration"))
    
    if "__name__ == \"__main__\"" in content:
        main_match = re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]:', content)
        if main_match:
            sections.append((main_match.start(), "Example Usage"))
    
    # Deduplicate sections based on title
    seen_titles = set()
    unique_sections = []
    for pos, title in sorted(sections, key=lambda x: x[0]):
        normalized_title = title.lower().strip()
        if normalized_title not in seen_titles:
            seen_titles.add(normalized_title)
            unique_sections.append((pos, title))
    
    # Sort by position in the file
    unique_sections.sort(key=lambda x: x[0])
    return unique_sections

def extract_sections(content, sections):
    """Extract content for each section."""
    section_contents = []
    for i, (pos, title) in enumerate(sections):
        # Find where this section ends
        end_pos = len(content)
        if i < len(sections) - 1:
            end_pos = sections[i+1][0]
        
        # Extract section content
        section_text = content[pos:end_pos].strip()
        
        # Skip if section is too short or just contains separator lines
        if len(section_text) > 10 and not all(line.startswith('#') for line in section_text.split('\n')):
            section_contents.append((title, section_text))
    
    return section_contents

def remove_duplicate_code(sections):
    """Remove duplicate code blocks from sections."""
    unique_sections = []
    seen_content = set()
    
    for title, content in sections:
        # Normalize content by removing comments and whitespace
        normalized_content = '\n'.join([
            line for line in content.split('\n') 
            if not line.strip().startswith('#') and line.strip()
        ])
        
        if normalized_content not in seen_content:
            seen_content.add(normalized_content)
            unique_sections.append((title, content))
        else:
            logger.info(f"Skipping duplicate section: {title}")
    
    return unique_sections

def create_notebook(py_file_path, output_notebook_path=None):
    """
    Convert Python file to Jupyter notebook with improved organization
    
    Args:
        py_file_path: Path to the Python file
        output_notebook_path: Path to save the notebook (optional)
    
    Returns:
        Path to the saved notebook
    """
    logger.info(f"Converting {py_file_path} to notebook")
    
    # Read the Python file
    with open(py_file_path, 'r') as f:
        content = f.read()
    
    # Extract docstring
    docstring, content = extract_docstring(content)
    
    # Create a new notebook
    notebook = nbf.v4.new_notebook()
    cells = []
    
    # Add title and description from docstring
    if docstring:
        title_line = docstring.split('\n')[0]
        description = '\n'.join(docstring.split('\n')[1:]).strip()
        
        title_cell = nbf.v4.new_markdown_cell(f"# {title_line}\n\n{description}")
        cells.append(title_cell)
    
    # Find section headers
    sections = find_section_headers(content)
    
    # Extract section contents
    section_contents = extract_sections(content, sections)
    
    # Remove duplicate sections
    unique_sections = remove_duplicate_code(section_contents)
    
    # Organize sections by component
    organized_sections = []
    
    # First add imports and configuration
    for title, section_text in unique_sections:
        if "Imports and Configuration" in title or "Docker service name" in title:
            organized_sections.append((title, section_text))
            
    # Add Knowledge Agent sections
    for title, section_text in unique_sections:
        if "Knowledge Agent" in title and title not in [s[0] for s in organized_sections]:
            organized_sections.append((title, section_text))
    
    # Add Card Agent sections
    for title, section_text in unique_sections:
        if "Card Agent" in title and title not in [s[0] for s in organized_sections]:
            organized_sections.append((title, section_text))
    
    # Add Orchestrator Agent sections
    for title, section_text in unique_sections:
        if "Orchestrator" in title and title not in [s[0] for s in organized_sections]:
            organized_sections.append((title, section_text))
    
    # Add Testing and Example Usage
    for title, section_text in unique_sections:
        if ("Testing" in title or "Example Usage" in title) and title not in [s[0] for s in organized_sections]:
            organized_sections.append((title, section_text))
    
    # Add any remaining sections
    for title, section_text in unique_sections:
        if title not in [s[0] for s in organized_sections]:
            organized_sections.append((title, section_text))
    
    # Add cells for each organized section
    for title, section_text in organized_sections:
        # Add a markdown cell for the section header
        cells.append(nbf.v4.new_markdown_cell(f"## {title}"))
        
        # Skip section separator lines and extract actual code
        lines = section_text.split('\n')
        filtered_lines = []
        for line in lines:
            if line.strip() and not (line.strip().startswith('#') and len(line.strip()) < 5):
                filtered_lines.append(line)
        
        code_chunk = '\n'.join(filtered_lines).strip()
        if code_chunk:
            cells.append(nbf.v4.new_code_cell(code_chunk))
    
    # Add cells to notebook
    notebook.cells = cells
    
    # Save the notebook
    if output_notebook_path is None:
        # Default to same name but with .ipynb extension
        base_name = os.path.splitext(os.path.basename(py_file_path))[0]
        output_dir = os.path.dirname(py_file_path)
        output_notebook_path = os.path.join(output_dir, f"{base_name}.ipynb")
    
    # Make sure the output directory exists
    os.makedirs(os.path.dirname(output_notebook_path), exist_ok=True)
    
    with open(output_notebook_path, 'w') as f:
        nbf.write(notebook, f)
    
    logger.info(f"Notebook created at: {output_notebook_path}")
    return output_notebook_path

def fix_notebook(notebook_path):
    """
    Fix the OpenAIEmbeddings import and chroma_api_impl setting in the notebook
    Also set the kernel specification to use the agentsenv kernel
    """
    logger.info(f"Fixing imports in notebook: {notebook_path}")
    
    # Read the notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)
    
    # Set the kernel to agentsenv
    notebook['metadata']['kernelspec'] = {
        "display_name": "Financial Agents (agentsenv)",
        "language": "python",
        "name": "agentsenv"
    }
    logger.info("Set kernel to 'agentsenv'")
    
    # Fix all occurrences of Path(__file__).parent in the notebook
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            cell_source = ''.join(cell['source'])
            if 'Path(__file__).parent' in cell_source:
                # Replace the problematic code in each line
                for i, line in enumerate(cell['source']):
                    if 'Path(__file__).parent' in line:
                        cell['source'][i] = line.replace('Path(__file__).parent', 'Path(os.path.abspath(""))')
    
    # Check if we need to add the path fix cell
    path_fix_found = False
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code' and 'Fix Python path' in ''.join(cell['source']):
            path_fix_found = True
            break
    
    # Add the path fix cell if it's not found
    if not path_fix_found:
        fix_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "source": [
                "# Fix Python path to ensure correct imports\n",
                "import sys\n",
                "import os\n",
                "from pathlib import Path\n",
                "\n",
                "# Add project root to sys.path to allow importing from parent directory\n",
                "current_dir = Path(os.path.abspath('')).parent\n",
                "if str(current_dir) not in sys.path:\n",
                "    sys.path.insert(0, str(current_dir))\n",
                "\n",
                "print(\"Path fixed for imports. Working directory:\", os.getcwd())\n"
            ],
            "outputs": []
        }
        notebook['cells'].insert(0, fix_cell)
    
    # Add debugging helpers cell
    debugging_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Debug Utilities\n",
            "\n",
            "The following functions provide detailed debugging output for each component."
        ]
    }
    
    debug_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "def debug_knowledge_retrieval(query):\n",
            "    \"\"\"Debug the knowledge retrieval process step by step.\"\"\"\n",
            "    print(f\"\\n=== DEBUGGING KNOWLEDGE RETRIEVAL FOR: '{query}' ===\\n\")\n",
            "    \n",
            "    # Initialize state\n",
            "    state = {\n",
            "        \"query\": query,\n",
            "        \"search_results\": [],\n",
            "        \"response\": \"\",\n",
            "        \"error\": None,\n",
            "        \"account_types\": [],\n",
            "        \"intent\": None\n",
            "    }\n",
            "    \n",
            "    # Extract account types\n",
            "    account_types = []\n",
            "    for account_type in [\"HSA\", \"FSA\", \"Health Savings Account\", \"Flexible Spending Account\", \n",
            "                       \"Dependent Care\", \"Prepaid\", \"Health Care Spend\"]:\n",
            "        if account_type.lower() in query.lower():\n",
            "            short_type = account_type\n",
            "            if account_type == \"Health Savings Account\":\n",
            "                short_type = \"HSA\"\n",
            "            elif account_type == \"Flexible Spending Account\":\n",
            "                short_type = \"FSA\"\n",
            "            \n",
            "            if short_type not in account_types:\n",
            "                account_types.append(short_type)\n",
            "    \n",
            "    print(f\"Detected account types: {account_types if account_types else 'None'}\")\n",
            "    \n",
            "    # Get vector store\n",
            "    print(\"\\nInitializing vector store...\")\n",
            "    vector_store = get_vector_store()\n",
            "    if vector_store:\n",
            "        print(\"✓ Vector store initialized successfully\")\n",
            "    else:\n",
            "        print(\"✗ Vector store initialization failed, will use mock data\")\n",
            "    \n",
            "    # Run intent classification\n",
            "    print(\"\\nClassifying query intent...\")\n",
            "    intent = classify_intent(query)\n",
            "    print(f\"Classified intent: {intent}\")\n",
            "    \n",
            "    # Run knowledge retrieval\n",
            "    print(\"\\nRetrieving knowledge...\")\n",
            "    updated_state = retrieve_knowledge(state)\n",
            "    \n",
            "    # Print search results\n",
            "    print(f\"\\nFound {len(updated_state['search_results'])} search results:\")\n",
            "    for i, result in enumerate(updated_state['search_results']):\n",
            "        print(f\"\\nResult {i+1}:\")\n",
            "        print(f\"Source: {result['source']}\")\n",
            "        if result['product_name']:\n",
            "            print(f\"Product: {result['product_name']}\")\n",
            "        print(f\"Text: {result['text'][:100]}...\")\n",
            "    \n",
            "    # Generate response\n",
            "    print(\"\\nGenerating response...\")\n",
            "    final_state = generate_response(updated_state)\n",
            "    \n",
            "    print(\"\\n=== FINAL RESPONSE ===\\n\")\n",
            "    print(final_state['response'])\n",
            "    \n",
            "    return final_state\n",
            "\n",
            "def debug_card_action(action, card_number, parameters=None):\n",
            "    \"\"\"Debug card action execution step by step.\"\"\"\n",
            "    if parameters is None:\n",
            "        parameters = {}\n",
            "        \n",
            "    print(f\"\\n=== DEBUGGING CARD ACTION: {action} for card {card_number} ===\\n\")\n",
            "    \n",
            "    # Initialize state\n",
            "    state = {\n",
            "        \"action\": action,\n",
            "        \"card_number\": card_number,\n",
            "        \"parameters\": parameters,\n",
            "        \"api_response\": None,\n",
            "        \"confirmation_message\": \"\",\n",
            "        \"error\": None\n",
            "    }\n",
            "    \n",
            "    print(f\"Card API URL: {CARD_API_BASE_URL}/{action}\")\n",
            "    print(f\"Payload: {{'cardLastFour': '{card_number}', **{parameters}}}\")\n",
            "    \n",
            "    # Mock the API call for debugging\n",
            "    print(\"\\nMocking API call for debugging purposes...\")\n",
            "    mock_result = {\n",
            "        \"success\": True,\n",
            "        \"message\": f\"Card {action} request processed for card ending in {card_number}\",\n",
            "        \"card\": {\n",
            "            \"lastFour\": card_number,\n",
            "            \"status\": \"ACTIVE\" if action == \"activate\" else \"INACTIVE\",\n",
            "            \"type\": \"HSA\",\n",
            "            \"expiryDate\": parameters.get(\"expiryDate\", \"12/25\")\n",
            "        }\n",
            "    }\n",
            "    \n",
            "    # Execute card action\n",
            "    print(\"\\nExecuting card action...\")\n",
            "    # Normally we'd call execute_card_action, but we'll use our mock for safety\n",
            "    result = {\n",
            "        **state,\n",
            "        \"api_response\": mock_result,\n",
            "        \"confirmation_message\": mock_result.get(\"message\"),\n",
            "        \"error\": None\n",
            "    }\n",
            "    \n",
            "    print(\"\\n=== RESULT ===\\n\")\n",
            "    print(f\"Confirmation: {result['confirmation_message']}\")\n",
            "    print(f\"API Response: {result['api_response']}\")\n",
            "    \n",
            "    return result\n",
            "\n",
            "def debug_orchestrator(query):\n",
            "    \"\"\"Debug the orchestrator's intent classification and routing.\"\"\"\n",
            "    print(f\"\\n=== DEBUGGING ORCHESTRATOR FOR QUERY: '{query}' ===\\n\")\n",
            "    \n",
            "    # Initialize state\n",
            "    state = {\n",
            "        \"user_query\": query,\n",
            "        \"intent\": \"unknown\",\n",
            "        \"card_action_details\": None,\n",
            "        \"knowledge_agent_response\": None,\n",
            "        \"card_agent_response\": None,\n",
            "        \"final_response\": \"\",\n",
            "        \"error\": None\n",
            "    }\n",
            "    \n",
            "    # Classify intent\n",
            "    print(\"Classifying intent...\")\n",
            "    classified_state = classify_intent(state)\n",
            "    print(f\"Classified intent: {classified_state['intent']}\")\n",
            "    \n",
            "    if classified_state['intent'] == 'card_action':\n",
            "        print(\"\\nCard action details:\")\n",
            "        details = classified_state['card_action_details']\n",
            "        if details:\n",
            "            print(f\"  Action: {details['action']}\")\n",
            "            print(f\"  Card Number: {details['card_number']}\")\n",
            "            print(f\"  Parameters: {details['parameters']}\")\n",
            "        else:\n",
            "            print(\"  No card details extracted\")\n",
            "    \n",
            "    # Determine routing\n",
            "    print(\"\\nDetermining routing...\")\n",
            "    route = decide_route(classified_state)\n",
            "    print(f\"Route decision: {route}\")\n",
            "    \n",
            "    # Execute the appropriate action based on route\n",
            "    if route == \"knowledge\":\n",
            "        print(\"\\nRouting to Knowledge Agent...\")\n",
            "        # Just call for a simple response for debugging\n",
            "        response = handle_query(query)\n",
            "        print(f\"\\nKnowledge Response: {response}\")\n",
            "        classified_state['knowledge_agent_response'] = response\n",
            "    elif route == \"card_action\" and classified_state['card_action_details']:\n",
            "        print(\"\\nRouting to Card Agent...\")\n",
            "        details = classified_state['card_action_details']\n",
            "        # Use our mock function\n",
            "        mock_result = debug_card_action(details['action'], details['card_number'], details['parameters'])\n",
            "        classified_state['card_agent_response'] = mock_result['confirmation_message']\n",
            "    \n",
            "    # Format the final response\n",
            "    print(\"\\nFormatting final response...\")\n",
            "    final_state = format_final_response(classified_state)\n",
            "    \n",
            "    print(\"\\n=== FINAL RESPONSE ===\\n\")\n",
            "    print(final_state['final_response'])\n",
            "    \n",
            "    return final_state\n"
        ],
        "outputs": []
    }
    
    notebook['cells'].append(debugging_cell)
    notebook['cells'].append(debug_code_cell)
    
    # Add a section for interactive testing
    interactive_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## Interactive Testing\n",
            "\n",
            "Test the components with your own queries and scenarios."
        ]
    }
    
    test_code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "source": [
            "# Test Knowledge Agent\n",
            "debug_knowledge_retrieval(\"What are the contribution limits for HSA accounts in 2024?\")\n",
            "\n",
            "# Test Card Agent\n",
            "debug_card_action(\"activate\", \"1234\", {\"cvv\": \"123\", \"expiryDate\": \"05/26\"})\n",
            "\n",
            "# Test Orchestrator with knowledge question\n",
            "debug_orchestrator(\"How do FSA accounts work?\")\n",
            "\n",
            "# Test Orchestrator with card action\n",
            "debug_orchestrator(\"I need to activate my card ending in 5678 with CVV 456\")"
        ],
        "outputs": []
    }
    
    notebook['cells'].append(interactive_cell)
    notebook['cells'].append(test_code_cell)
    
    # Process each cell
    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            # Fix OpenAIEmbeddings import
            for i, line in enumerate(cell['source']):
                if "from langchain_community.embeddings import OpenAIEmbeddings" in line:
                    cell['source'][i] = line.replace(
                        "from langchain_community.embeddings import OpenAIEmbeddings",
                        "from langchain_openai import OpenAIEmbeddings"
                    )
                
                # Fix chroma_api_impl
                if 'chroma_api_impl="rest" if not USE_PERSISTENT else "duckdb+parquet"' in line:
                    cell['source'][i] = line.replace(
                        'chroma_api_impl="rest" if not USE_PERSISTENT else "duckdb+parquet"',
                        'chroma_api_impl="duckdb+parquet"'
                    )
                
                # Fix __file__ not defined error
                if 'Path(__file__).parent' in line:
                    cell['source'][i] = line.replace(
                        'Path(__file__).parent',
                        'Path(os.path.abspath(""))'
                    )
    
    # Save the notebook
    with open(notebook_path, 'w') as f:
        json.dump(notebook, f, indent=1)
    
    logger.info(f"Fixed imports, configuration, and set kernel in {notebook_path}")
    return notebook_path

def main():
    """Main function to convert and fix a Python file to notebook."""
    parser = argparse.ArgumentParser(description="Convert Python file to Jupyter notebook and fix imports.")
    parser.add_argument('--input', type=str, default='merged_agents.py', help='Input Python file')
    parser.add_argument('--output', type=str, default='notebooks/merged_financial_agents.ipynb', help='Output notebook file')
    parser.add_argument('--fix-existing', action='store_true', help='Only fix an existing notebook without converting')
    args = parser.parse_args()
    
    if args.fix_existing:
        # Just fix the existing notebook
        if not os.path.exists(args.output):
            logger.error(f"Notebook {args.output} not found")
            return 1
        fix_notebook(args.output)
    else:
        # Convert the Python file to a notebook
        notebook_path = create_notebook(args.input, args.output)
        
        # Fix the notebook
        fix_notebook(notebook_path)
    
    logger.info("Notebook created and fixed successfully")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 