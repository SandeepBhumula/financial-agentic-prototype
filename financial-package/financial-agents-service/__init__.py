"""Financial Agents package for AI-powered financial services."""

# Package metadata
__package_name__ = "financial_agents"
__version__ = "0.1.0"

# Import main components
from .core.orchestrator import app as orchestrator_app
from .core.card import card_agent_app
from .core.knowledge import knowledge_agent_app

# Make modules accessible
from . import core
from . import data
from . import ui
from . import vector_db

__all__ = [
    'orchestrator_app', 
    'card_agent_app', 
    'knowledge_agent_app',
    'core',
    'data',
    'ui',
    'vector_db'
] 