"""Data resources for the Financial Agents package."""

import os
import json

# Path to financial products data
FINANCIAL_PRODUCTS_PATH = os.path.join(os.path.dirname(__file__), 'financial_products.json')

def load_financial_products():
    """Load financial products data from JSON file."""
    with open(FINANCIAL_PRODUCTS_PATH, 'r') as f:
        return json.load(f) 