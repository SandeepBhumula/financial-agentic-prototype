import json
import os

def generate_data():
    """Generates synthetic financial product data."""
    data = {
        "products": [
            {
                "id": "HSA001",
                "name": "Health Savings Account (HSA)",
                "description": "A tax-advantaged savings account for individuals with high-deductible health plans (HDHPs). Funds can be used for qualified medical expenses.",
                "eligibility": "Must be covered under an HDHP, not enrolled in Medicare, and cannot be claimed as a dependent on someone else's tax return.",
                "contribution_limit_individual": 3850, # Example for 2023, update as needed
                "contribution_limit_family": 7750, # Example for 2023, update as needed
                "features": ["Tax-deductible contributions", "Tax-free growth", "Tax-free withdrawals for qualified medical expenses", "Funds roll over year to year"]
            },
            {
                "id": "FSA001",
                "name": "Flexible Spending Account (FSA)",
                "description": "An employer-sponsored account allowing employees to set aside pre-tax dollars for eligible healthcare or dependent care expenses.",
                "eligibility": "Offered by employer; specific eligibility criteria may apply.",
                "contribution_limit": 3050, # Example for 2023 healthcare FSA, update as needed
                "features": ["Pre-tax contributions reduce taxable income", "Funds available immediately at the start of the plan year"],
                "notes": "Generally subject to 'use-it-or-lose-it' rule, though some plans offer carryover or grace periods."
            },
            {
                "id": "PREPAID001",
                "name": "General Purpose Prepaid Card",
                "description": "A reloadable card not linked to a bank account, usable wherever the card network (e.g., Visa, Mastercard) is accepted.",
                "eligibility": "Generally available to anyone, subject to identity verification.",
                "features": ["Budgeting tool", "Alternative to traditional bank accounts", "Can be used for online purchases"],
                "fees": ["Activation fee", "Monthly maintenance fee", "Reload fee", "ATM withdrawal fee (may vary)"]
            },
            {
                "id": "HCSA001",
                "name": "Health Care Spending Account (HCSA)",
                "description": "Often used interchangeably with Health FSA, but sometimes refers to specific employer-funded arrangements like Health Reimbursement Arrangements (HRAs). Focuses on reimbursing eligible medical expenses.",
                "eligibility": "Dependent on specific employer plan (FSA or HRA).",
                "features": ["Typically funded by employer (HRA) or employee pre-tax (FSA)", "Used for qualified medical expenses as defined by the IRS"],
                "notes": "Rules vary significantly based on whether it's an FSA or HRA."

            }
        ]
    }
    return data

def save_data(data, output_dir="src/data", filename="financial_products.json"):
    """Saves the generated data to a JSON file."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Synthetic data saved to {filepath}")

if __name__ == "__main__":
    synthetic_data = generate_data()
    save_data(synthetic_data) 