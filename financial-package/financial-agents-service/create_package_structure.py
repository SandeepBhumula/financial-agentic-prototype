#!/usr/bin/env python3
"""
Create Package Structure

This script creates the necessary directory structure and initializes
the financial_agents package structure properly.
"""

import os
import sys
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

INIT_CONTENT = """\"\"\"
Financial Agents Package

This package provides LangGraph-based agents for financial services.
\"\"\"

# Import the individual agents from the merged implementation
from merged_agents import (
    # Knowledge Agent
    KnowledgeAgentState,
    knowledge_agent,
    handle_query,
    
    # Card Agent
    CardAgentState,
    card_agent_app,
    
    # Orchestrator Agent
    OrchestratorState,
    orchestrator_app,
    
    # Testing functions
    test_knowledge_agent,
    test_card_agent,
    test_orchestrator
)

__all__ = [
    # Knowledge Agent
    'KnowledgeAgentState',
    'knowledge_agent',
    'handle_query',
    
    # Card Agent
    'CardAgentState',
    'card_agent_app',
    
    # Orchestrator Agent
    'OrchestratorState',
    'orchestrator_app',
    
    # Testing functions
    'test_knowledge_agent',
    'test_card_agent',
    'test_orchestrator'
]
"""

def create_package_structure():
    """Create the necessary package structure."""
    # Get current directory
    root_dir = Path(__file__).parent
    
    # Create directories if they don't exist
    directories = [
        root_dir / "financial_agents",
        root_dir / "notebooks",
        root_dir / "data" / "chroma_db",
        root_dir / "core",
        root_dir / "ui",
        root_dir / "vector_db",
        root_dir / "tests"
    ]
    
    for directory in directories:
        if not directory.exists():
            logger.info(f"Creating directory: {directory}")
            directory.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py files
    init_files = [
        root_dir / "financial_agents" / "__init__.py",
        root_dir / "core" / "__init__.py",
        root_dir / "ui" / "__init__.py",
        root_dir / "vector_db" / "__init__.py",
        root_dir / "tests" / "__init__.py"
    ]
    
    for init_file in init_files:
        if not init_file.exists():
            logger.info(f"Creating file: {init_file}")
            if init_file == root_dir / "financial_agents" / "__init__.py":
                with open(init_file, "w") as f:
                    f.write(INIT_CONTENT)
            else:
                # Create empty __init__.py for other directories
                init_file.touch()
    
    logger.info("Package structure created successfully")
    return 0

if __name__ == "__main__":
    sys.exit(create_package_structure()) 