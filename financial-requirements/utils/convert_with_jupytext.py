#!/usr/bin/env python
"""
Script to convert notebook-formatted Python files to Jupyter notebooks using jupytext.
This is a simpler and more robust approach than using nbformat directly.
"""

import sys
from pathlib import Path
import jupytext

def convert_py_to_notebook(py_file_path, output_path=None):
    """Convert a Python file with notebook cell markers to a Jupyter notebook using jupytext."""
    if output_path is None:
        output_path = Path(py_file_path).with_suffix('.ipynb')
    else:
        output_path = Path(output_path)
    
    # Read the notebook from the Python file
    notebook = jupytext.read(py_file_path)
    
    # Write the notebook as an .ipynb file
    jupytext.write(notebook, output_path)
    
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