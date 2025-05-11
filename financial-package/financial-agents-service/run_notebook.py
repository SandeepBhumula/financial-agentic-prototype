#!/usr/bin/env python3
"""
Run Notebook Utility

This script fixes and runs the financial agents Jupyter notebook,
ensuring all imports work correctly regardless of Python version.

Usage:
    python run_notebook.py
"""

import os
import sys
import subprocess
import platform
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_python_version():
    """Check if the Python version is compatible with our requirements"""
    version = platform.python_version()
    logger.info(f"Using Python version: {version}")
    
    if version == "3.9.7":
        logger.warning("Python 3.9.7 has known compatibility issues with streamlit")
        logger.warning("The notebook should still run, but UI components might fail")
    
    return version

def setup_environment():
    """Set up the environment by installing necessary packages"""
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    
    if not in_venv:
        logger.info("Creating a virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "notebook-venv"], check=True)
            
            # Determine the activation script based on platform
            if platform.system() == "Windows":
                activate_script = os.path.join("notebook-venv", "Scripts", "activate")
            else:
                activate_script = os.path.join("notebook-venv", "bin", "activate")
            
            logger.info(f"Virtual environment created. Activate with: source {activate_script}")
            logger.info("Then run this script again.")
            return False
        except Exception as e:
            logger.error(f"Failed to create virtual environment: {e}")
            return False
    
    # Install required packages if needed
    try:
        logger.info("Installing required packages...")
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "jupyter", "nbformat", "ipykernel", 
            "openai", "langchain", "langchain-core", "langchain-openai", 
            "pydantic", "chromadb", "langchain-chroma"
        ], check=True)
        
        # Register the kernel if needed
        logger.info("Registering Jupyter kernel...")
        subprocess.run([
            sys.executable, "-m", "ipykernel", "install", "--user",
            "--name=financial-agents", "--display-name=Financial Agents Environment"
        ], check=True)
        
        return True
    except Exception as e:
        logger.error(f"Failed to install packages: {e}")
        return False

def fix_notebook():
    """Fix the notebook to ensure imports work correctly"""
    notebook_path = Path("notebooks/merged_financial_agents.ipynb")
    
    if not notebook_path.exists():
        logger.error(f"Notebook not found at {notebook_path}")
        return False
    
    try:
        # First check if notebook_util.py exists and use it if available
        if Path("notebook_util.py").exists():
            logger.info("Using notebook_util.py to fix notebook...")
            subprocess.run([
                sys.executable, "notebook_util.py", 
                "--fix-existing", "--output", str(notebook_path)
            ], check=True)
        else:
            # If notebook_util.py doesn't exist, we'll need to manually fix the notebook
            logger.info("notebook_util.py not found, using direct fixes...")
            
            import json
            with open(notebook_path, 'r') as f:
                notebook = json.load(f)
            
            # Add path fixing cell if needed
            path_fix_found = False
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code' and 'Fix Python path' in ''.join(cell['source']):
                    path_fix_found = True
                    break
            
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
                        "# Add current directory's parent to sys.path\n",
                        "current_dir = Path(os.path.abspath('')).parent\n",
                        "if str(current_dir) not in sys.path:\n",
                        "    sys.path.insert(0, str(current_dir))\n",
                        "\n",
                        "print(\"Path fixed for imports. Working directory:\", os.getcwd())\n"
                    ],
                    "outputs": []
                }
                notebook['cells'].insert(0, fix_cell)
            
            # Fix imports in each cell
            for cell in notebook['cells']:
                if cell['cell_type'] == 'code':
                    for i, line in enumerate(cell['source']):
                        # Fix OpenAIEmbeddings import
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
            
            # Save the notebook
            with open(notebook_path, 'w') as f:
                json.dump(notebook, f, indent=1)
        
        logger.info("Notebook successfully fixed")
        return True
    except Exception as e:
        logger.error(f"Failed to fix notebook: {e}")
        return False

def run_notebook():
    """Run the Jupyter notebook"""
    try:
        # First check if the kernel exists
        kernel_exists = False
        try:
            kernels_output = subprocess.check_output([sys.executable, "-m", "jupyter", "kernelspec", "list"])
            kernel_exists = "financial-agents" in kernels_output.decode()
        except Exception:
            kernel_exists = False
        
        if not kernel_exists:
            logger.warning("Financial Agents kernel not found, registering...")
            subprocess.run([
                sys.executable, "-m", "ipykernel", "install", "--user",
                "--name=financial-agents", "--display-name=Financial Agents Environment"
            ], check=True)
        
        # Launch Jupyter notebook
        notebook_path = os.path.join("notebooks", "merged_financial_agents.ipynb")
        
        if platform.system() == "Windows":
            cmd = f'start cmd /c "{sys.executable} -m jupyter notebook {notebook_path}"'
            os.system(cmd)
        else:
            cmd = [sys.executable, "-m", "jupyter", "notebook", notebook_path]
            subprocess.Popen(cmd)
        
        logger.info("Notebook launched. Please select the 'Financial Agents Environment' kernel.")
        logger.info("Remember to run the first code cell which fixes the import paths.")
        return True
    except Exception as e:
        logger.error(f"Failed to run notebook: {e}")
        return False

def main():
    """Main function to fix and run the notebook"""
    logger.info("Starting Financial Agents notebook setup and run utility")
    
    # Check Python version
    check_python_version()
    
    # Make sure notebooks directory exists
    os.makedirs("notebooks", exist_ok=True)
    
    # Setup environment
    if not setup_environment():
        logger.error("Failed to set up environment. Please check the logs.")
        return 1
    
    # Fix notebook
    if not fix_notebook():
        logger.error("Failed to fix notebook. Please check the logs.")
        return 1
    
    # Run notebook
    if not run_notebook():
        logger.error("Failed to run notebook. Please check the logs.")
        return 1
    
    logger.info("Setup completed successfully. The notebook should be running now.")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 