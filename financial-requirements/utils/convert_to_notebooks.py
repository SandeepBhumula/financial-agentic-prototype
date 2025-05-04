#!/usr/bin/env python
"""
Script to convert notebook-formatted Python files to Jupyter notebooks.
This handles files with # %% cell markers and # %% [markdown] markdown cells.
"""

import nbformat
import re
import sys
from pathlib import Path

def convert_py_to_notebook(py_file_path, output_path=None):
    """Convert a Python file with notebook cell markers to a Jupyter notebook."""
    if output_path is None:
        output_path = Path(py_file_path).with_suffix('.ipynb')
    else:
        output_path = Path(output_path)
    
    # Read the Python file
    with open(py_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Create a new notebook
    nb = nbformat.v4.new_notebook()
    cells = []
    
    # Split the content at cell markers
    cell_pattern = r'# %%.*?\n(.*?)(?=# %%|$)'
    markdown_pattern = r'# %% \[markdown\].*?\n(.*?)(?=# %%|$)'
    
    # Find all cells
    for cell_match in re.finditer(cell_pattern, content, re.DOTALL):
        cell_content = cell_match.group(1).strip()
        
        # Check if it's a markdown cell
        if re.match(r'# %% \[markdown\]', cell_match.group(0)):
            # Remove any leading #s from markdown content lines
            cleaned_content = '\n'.join([line.lstrip('# ') for line in cell_content.split('\n')])
            cells.append(nbformat.v4.new_markdown_cell(cleaned_content))
        else:
            cells.append(nbformat.v4.new_code_cell(cell_content))
    
    nb.cells = cells
    
    # Write the notebook to file
    with open(output_path, 'w', encoding='utf-8') as file:
        nbformat.write(nb, file)
    
    print(f"Converted {py_file_path} to {output_path}")

if __name__ == "__main__":
    # Check if files were specified on the command line
    if len(sys.argv) > 1:
        for py_file in sys.argv[1:]:
            convert_py_to_notebook(py_file)
    else:
        # If no files specified, convert the default agent notebook files
        files_to_convert = [
            "knowledge_agent_notebook.py",
            "orchestrator_agent_notebook.py"
        ]
        
        for py_file in files_to_convert:
            convert_py_to_notebook(py_file) 