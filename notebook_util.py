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

def fix_notebook_path():
    """
    Generate a code cell that fixes Python path for imports in notebooks.
    This should be added as the first cell in the notebook.
    """
    return nbf.v4.new_code_cell("""
# Fix Python path to ensure correct imports
import sys
import os
from pathlib import Path

# Add project root to sys.path to allow importing from parent directory
current_dir = Path(os.path.abspath('')).parent
if str(current_dir) not in sys.path:
    sys.path.insert(0, str(current_dir))

print("Path fixed for imports. Working directory:", os.getcwd())
""")

def extract_docstring(content):
    """Extract the docstring from the Python file."""
    docstring_match = re.match(r'"""(.*?)"""', content, re.DOTALL)
    if docstring_match:
        return docstring_match.group(1).strip(), content[docstring_match.end():]
    return None, content

def find_section_headers(content):
    """Find section headers in the Python file."""
    # Match section headers like "# --- Section Name ---" or "#################################################"
    section_patterns = [
        r'#\s*---\s*(.*?)\s*---\s*#*', 
        r'#\s*(.*?)\s*#+'  # For headers surrounded by hashes
    ]
    
    sections = []
    for pattern in section_patterns:
        for match in re.finditer(pattern, content):
            section_title = match.group(1).strip()
            if section_title and not section_title.startswith("---"):
                sections.append((match.start(), section_title))
    
    # Get other major sections (import blocks, main block)
    if "import " in content:
        import_match = re.search(r'import\s+', content)
        if import_match:
            sections.append((import_match.start(), "Imports and Configuration"))
    
    if "if __name__ == \"__main__\":" in content:
        main_match = re.search(r'if\s+__name__\s*==\s*[\'"]__main__[\'"]:', content)
        if main_match:
            sections.append((main_match.start(), "Example Usage"))
    
    # Sort by position in the file
    sections.sort(key=lambda x: x[0])
    return sections

def create_notebook(py_file_path, output_notebook_path=None):
    """
    Convert Python file to Jupyter notebook
    
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
    
    # Add the path fixing cell at the very beginning
    cells.append(fix_notebook_path())
    
    # Add title and description from docstring
    if docstring:
        title_line = docstring.split('\n')[0]
        description = '\n'.join(docstring.split('\n')[1:]).strip()
        
        title_cell = nbf.v4.new_markdown_cell(f"# {title_line}\n\n{description}")
        cells.append(title_cell)
    
    # Find section headers
    sections = find_section_headers(content)
    
    # Add cells for each section
    if sections:
        start_pos = 0
        
        for i, (pos, title) in enumerate(sections):
            # Add the code before this section (if any)
            if pos > start_pos:
                code_chunk = content[start_pos:pos].strip()
                if code_chunk:
                    cells.append(nbf.v4.new_code_cell(code_chunk))
            
            # Add a markdown cell for the section header
            cells.append(nbf.v4.new_markdown_cell(f"## {title}"))
            
            # Update start position for next chunk
            start_pos = pos
            
            # Find where this section ends
            if i < len(sections) - 1:
                next_pos = sections[i+1][0]
                
                # Find the first line break after the header
                header_end = content.find('\n', pos) + 1
                if header_end > 0:
                    code_chunk = content[header_end:next_pos].strip()
                    if code_chunk:
                        cells.append(nbf.v4.new_code_cell(code_chunk))
            else:
                # This is the last section
                header_end = content.find('\n', pos) + 1
                if header_end > 0:
                    code_chunk = content[header_end:].strip()
                    if code_chunk:
                        cells.append(nbf.v4.new_code_cell(code_chunk))
    else:
        # No sections found, just add the whole content as a code cell
        cells.append(nbf.v4.new_code_cell(content))
    
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