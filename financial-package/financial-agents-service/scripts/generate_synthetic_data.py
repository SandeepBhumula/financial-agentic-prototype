#!/usr/bin/env python3
"""
Generate synthetic healthcare financial data for the vector database.
This script uses SDV (Synthetic Data Vault) to create realistic financial 
data for healthcare accounts like HSA, FSA, etc.
"""

import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sdv.single_table import GaussianCopulaSynthesizer
from sdv.metadata import SingleTableMetadata
import random

# Constants - reduced for MB size instead of GB
NUM_RECORDS = 5000
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
ACCOUNTS_FILE = os.path.join(OUTPUT_DIR, 'synthetic_healthcare_accounts.csv')
TRANSACTIONS_FILE = os.path.join(OUTPUT_DIR, 'synthetic_healthcare_transactions.csv')
PRODUCTS_FILE = os.path.join(OUTPUT_DIR, 'synthetic_healthcare_products.json')
PLANS_FILE = os.path.join(OUTPUT_DIR, 'synthetic_healthcare_plans.json')

# Ensure the output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_transaction_text(account_type, annual_spend, num_transactions=None):
    """Generate realistic transaction text based on account type and spending amount."""
    categories = {
        'HSA': [
            'Doctor visit', 'Prescription medication', 'Lab test', 'Medical equipment', 
            'Dental care', 'Vision care', 'Chiropractic treatment', 'Physical therapy'
        ],
        'FSA': [
            'Copayment', 'Deductible payment', 'Over-the-counter medication', 
            'First aid supplies', 'Contact lens solution', 'Sunscreen'
        ],
        'Dependent Care': [
            'Daycare center', 'After-school program', 'Summer camp', 'Adult day care', 
            'In-home caregiver', 'Preschool tuition'
        ],
        'Prepaid': [
            'Hospital payment', 'Urgent care visit', 'Specialist consultation', 
            'Physical therapy', 'Preventive care', 'Imaging services'
        ],
        'Health Care Spend': [
            'Premium payment', 'Coinsurance payment', 'Medicare Part D payment',
            'COBRA premium', 'Marketplace plan premium'
        ]
    }
    
    if num_transactions is None:
        # Generate 3-10 transactions
        num_transactions = random.randint(3, 10)
    
    transactions = []
    remaining_spend = annual_spend
    
    for i in range(num_transactions):
        # Last transaction uses remaining spend
        if i == num_transactions - 1:
            amount = remaining_spend
        else:
            # Generate random transaction amount
            amount = round(random.uniform(20, remaining_spend * 0.3), 2)
            remaining_spend -= amount
            
        if remaining_spend <= 0:
            break
            
        category = random.choice(categories.get(account_type, categories['HSA']))
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
        status = random.choice(['Approved', 'Pending', 'Cleared'])
        
        transaction = {
            "date": date,
            "amount": amount,
            "category": category,
            "status": status
        }
        
        transactions.append(transaction)
    
    return transactions

def generate_product_details():
    """Generate detailed information about healthcare financial products."""
    products = [
        {
            "id": "HSA001",
            "name": "Health Savings Account (HSA)",
            "description": "A tax-advantaged savings account for individuals with high-deductible health plans (HDHPs). Funds can be used for qualified medical expenses with triple tax advantages.",
            "eligibility_requirements": [
                "Must be enrolled in an HDHP with a minimum deductible of $1,500 for individuals or $3,000 for families",
                "Cannot be enrolled in Medicare",
                "Cannot be claimed as a dependent on someone else's tax return"
            ],
            "contribution_limits": {
                "individual": {
                    "2023": 3850,
                    "2024": 4150
                },
                "family": {
                    "2023": 7750,
                    "2024": 8300
                },
                "catch_up_age": 55,
                "catch_up_amount": 1000
            },
            "features": [
                "Tax-deductible contributions",
                "Tax-free growth",
                "Tax-free withdrawals for qualified medical expenses",
                "Funds roll over year to year",
                "Portable between employers",
                "Investment options for long-term growth"
            ],
            "qualified_expenses": [
                "Doctor visits and consultations",
                "Hospital services",
                "Dental care",
                "Vision care",
                "Prescription medications",
                "Over-the-counter medications (with prescription)",
                "Medical equipment and supplies"
            ]
        },
        {
            "id": "FSA001",
            "name": "Flexible Spending Account (FSA)",
            "description": "An employer-sponsored account allowing employees to set aside pre-tax dollars for eligible healthcare or dependent care expenses.",
            "types": [
                {
                    "name": "Healthcare FSA",
                    "description": "For qualified medical expenses"
                },
                {
                    "name": "Limited Purpose FSA",
                    "description": "For dental and vision expenses only, can be used alongside an HSA"
                },
                {
                    "name": "Dependent Care FSA",
                    "description": "For eligible dependent care expenses"
                }
            ],
            "eligibility_requirements": [
                "Must be offered by employer",
                "Self-employed individuals are not eligible",
                "Healthcare FSA may not be compatible with HSA"
            ],
            "contribution_limits": {
                "healthcare_fsa": {
                    "2023": 3050,
                    "2024": 3200
                },
                "dependent_care_fsa": {
                    "individual_or_married_filing_jointly": 5000,
                    "married_filing_separately": 2500
                }
            },
            "features": [
                "Pre-tax contributions reduce taxable income",
                "Funds available immediately at the start of the plan year"
            ]
        },
        {
            "id": "DCA001",
            "name": "Dependent Care Assistance Program (DCAP)",
            "description": "A benefit plan that allows employees to pay for eligible dependent care expenses with pre-tax dollars.",
            "eligibility_requirements": [
                "Must be offered by employer",
                "You and your spouse must be employed, looking for work, or attending school full-time",
                "The dependent must be a qualifying child under 13 or a disabled dependent or spouse"
            ],
            "contribution_limits": {
                "married_filing_jointly": 5000,
                "single_or_head_of_household": 5000,
                "married_filing_separately": 2500
            },
            "qualified_expenses": [
                "Daycare centers",
                "Preschool (not kindergarten or higher)",
                "Summer day camps",
                "Before and after-school programs",
                "Nannies and babysitters (if work-related)"
            ]
        },
        {
            "id": "PREPAID001",
            "name": "Healthcare Prepaid Card",
            "description": "A specialized payment card loaded with funds from healthcare accounts like HSAs, FSAs, or HRAs.",
            "types": [
                {
                    "name": "HSA Debit Card",
                    "description": "Linked to Health Savings Account"
                },
                {
                    "name": "FSA Debit Card",
                    "description": "Linked to Flexible Spending Account"
                },
                {
                    "name": "HRA Card",
                    "description": "Linked to Health Reimbursement Arrangement"
                }
            ],
            "features": [
                "Immediate payment at point of service",
                "Auto-substantiation at eligible merchants",
                "Reduces need for manual claim submission"
            ]
        },
        {
            "id": "HCSPEND001",
            "name": "Healthcare Spending Account",
            "description": "A general term for accounts that help consumers pay for healthcare expenses.",
            "common_types": [
                "Health Savings Account (HSA)",
                "Flexible Spending Account (FSA)",
                "Health Reimbursement Arrangement (HRA)",
                "Medicare Medical Savings Account (MSA)"
            ],
            "key_considerations": [
                "Tax advantages",
                "Contribution limits",
                "Eligible expenses",
                "Account ownership",
                "Rollover policies",
                "Investment options"
            ]
        }
    ]
    
    # Add some basic plan options for each product type
    plans = []
    
    # HSA Plans
    hsa_providers = ["HealthEquity", "Fidelity", "Optum Bank", "HSA Bank"]
    for provider in hsa_providers:
        plans.append({
            "product_id": "HSA001",
            "provider": provider,
            "plan_name": f"{provider} Health Savings Account",
            "monthly_fee": random.choice([0, 2.50, 3.45, 4.95]),
            "interest_rate": round(random.uniform(0.01, 0.5), 2),
            "investment_options": random.choice([True, True, False]),
            "debit_card": True
        })
    
    # FSA Plans
    fsa_providers = ["WageWorks", "ConnectYourCare", "BenefitWallet"]
    for provider in fsa_providers:
        plans.append({
            "product_id": "FSA001",
            "provider": provider,
            "plan_name": f"{provider} Flexible Spending Account",
            "grace_period": random.choice([True, False]),
            "carryover": random.choice([True, False]) if not plans[-1].get("grace_period", False) else False,
            "carryover_amount": random.randint(500, 610) if plans[-1].get("carryover", False) else 0,
            "debit_card": True
        })
    
    return products, plans

def create_real_data_sample():
    """Create a small sample of 'real' data to train the synthesizer."""
    account_types = ['HSA', 'FSA', 'Dependent Care', 'Prepaid', 'Health Care Spend']
    
    # 2024 contribution limits
    contribution_limits = {
        'HSA': [4150, 8300],  # Individual, Family
        'FSA': [3200, 3200],
        'Dependent Care': [5000, 5000],
        'Prepaid': [10000, 10000],  # No real limit, just using a placeholder
        'Health Care Spend': [15000, 25000]  # General healthcare spending, placeholder
    }
    
    data = []
    
    for i in range(200):  # Create 200 sample records for training
        account_type = random.choice(account_types)
        
        # 30% chance of family account for HSA
        is_family = (account_type == 'HSA' and random.random() < 0.3) or random.random() < 0.2
        
        # Set contribution limit based on account type and individual/family
        limit_idx = 1 if is_family else 0
        contribution_limit = contribution_limits[account_type][limit_idx]
        
        # Annual spend is a percentage of the contribution limit
        spend_percentage = random.uniform(0.2, 0.9)
        annual_spend = round(contribution_limit * spend_percentage, 2)
        
        # Generate transaction history
        transactions = generate_transaction_text(account_type, annual_spend)
        
        # User ID (simplified)
        user_id = f"USER{random.randint(1000, 9999)}"
        
        account_data = {
            'account_id': f"{account_type[0]}{random.randint(10000, 99999)}",
            'user_id': user_id,
            'account_type': account_type,
            'account_subtype': 'Family' if is_family else 'Individual',
            'contribution_limit': contribution_limit,
            'annual_spend': annual_spend,
            'remaining_balance': round(contribution_limit - annual_spend, 2),
            'num_transactions': len(transactions),
            'average_transaction': round(annual_spend / len(transactions), 2) if transactions else 0,
            'creation_date': (datetime.now() - timedelta(days=random.randint(30, 1825))).strftime('%Y-%m-%d'),
            'plan_year_start': f"{datetime.now().year}-01-01",
            'plan_year_end': f"{datetime.now().year}-12-31",
            'has_debit_card': random.choice([True, True, False]),
            'investment_enabled': account_type == 'HSA' and random.choice([True, False])
        }
        
        data.append(account_data)
    
    return pd.DataFrame(data)

def generate_users(num_users=200):
    """Generate synthetic user profiles to associate with accounts."""
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", "William", "Elizabeth"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Miller", "Davis", "Garcia", "Rodriguez", "Wilson"]
    
    users = []
    for i in range(num_users):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        birth_year = random.randint(1960, 2000)
        age = datetime.now().year - birth_year
        
        user = {
            "user_id": f"USER{i+1000}",
            "first_name": first_name,
            "last_name": last_name,
            "email": f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}@example.com",
            "birth_year": birth_year,
            "age": age,
            "marital_status": random.choice(["Single", "Married", "Divorced", "Widowed"]),
            "has_dependents": random.choice([True, False, False, True]),
            "num_dependents": random.randint(1, 4) if users and users[-1].get("has_dependents", False) else random.randint(0, 3),
            "employment_status": random.choice(["Full-time", "Part-time", "Contract", "Retired"]),
            "income_bracket": random.choice(["Under $50k", "$50k-$100k", "$100k-$150k", "Over $150k"]),
            "zip_code": f"{random.randint(10000, 99999)}",
            "state": random.choice(["CA", "TX", "FL", "NY", "IL", "PA", "OH", "GA", "NC", "MI"])
        }
        users.append(user)
    
    return users

def generate_synthetic_data():
    """Generate synthetic healthcare financial data."""
    print("Generating synthetic healthcare financial data...")
    
    # Create products and plans
    products, plans = generate_product_details()
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump({"products": products}, f, indent=2)
    print(f"Saved {len(products)} product details to {PRODUCTS_FILE}")
    
    with open(PLANS_FILE, 'w') as f:
        json.dump({"plans": plans}, f, indent=2)
    print(f"Saved {len(plans)} plan details to {PLANS_FILE}")
    
    # Generate users
    users = generate_users(200)
    with open(os.path.join(OUTPUT_DIR, 'synthetic_healthcare_users.json'), 'w') as f:
        json.dump({"users": users}, f, indent=2)
    print(f"Saved {len(users)} user profiles")
    
    # Create metadata for the account synthesizer
    account_metadata = SingleTableMetadata()
    account_metadata.add_column('account_id', sdtype='id')
    account_metadata.add_column('user_id', sdtype='id')
    account_metadata.add_column('account_type', sdtype='categorical')
    account_metadata.add_column('account_subtype', sdtype='categorical')
    account_metadata.add_column('contribution_limit', sdtype='numerical')
    account_metadata.add_column('annual_spend', sdtype='numerical')
    account_metadata.add_column('remaining_balance', sdtype='numerical')
    account_metadata.add_column('num_transactions', sdtype='numerical')
    account_metadata.add_column('average_transaction', sdtype='numerical')
    account_metadata.add_column('creation_date', sdtype='datetime')
    account_metadata.add_column('plan_year_start', sdtype='datetime')
    account_metadata.add_column('plan_year_end', sdtype='datetime')
    account_metadata.add_column('has_debit_card', sdtype='boolean')
    account_metadata.add_column('investment_enabled', sdtype='boolean')
    
    # Create sample real data to train the synthesizer
    real_data = create_real_data_sample()
    
    # Initialize and fit the account synthesizer
    print("Training the synthesizer on sample data...")
    account_synthesizer = GaussianCopulaSynthesizer(account_metadata)
    account_synthesizer.fit(real_data)
    
    # Generate synthetic account data
    print(f"Generating {NUM_RECORDS} synthetic account records...")
    synthetic_accounts = account_synthesizer.sample(num_rows=NUM_RECORDS)
    
    # Ensure account_id is unique
    synthetic_accounts['account_id'] = [f"ACC{i:06d}" for i in range(len(synthetic_accounts))]
    
    # Assign random user IDs from our user pool
    synthetic_accounts['user_id'] = [random.choice(users)["user_id"] for _ in range(len(synthetic_accounts))]
    
    # Generate transaction data for each account
    print("Generating transaction data...")
    all_transactions = []
    for _, account in synthetic_accounts.iterrows():
        num_txn = int(account['num_transactions'])
        if num_txn > 0:
            transactions = generate_transaction_text(
                account['account_type'], 
                account['annual_spend'], 
                min(num_txn, 10)  # Limit to 10 transactions per account for smaller dataset
            )
            
            for idx, txn in enumerate(transactions):
                txn_data = txn.copy()
                txn_data.update({
                    'transaction_id': f"TXN{account['account_id']}{idx:04d}",
                    'account_id': account['account_id'],
                    'user_id': account['user_id']
                })
                all_transactions.append(txn_data)
    
    # Save accounts
    synthetic_accounts.to_csv(ACCOUNTS_FILE, index=False)
    print(f"Saved {len(synthetic_accounts)} account records to {ACCOUNTS_FILE}")
    
    # Save transactions
    transactions_df = pd.DataFrame(all_transactions)
    transactions_df.to_csv(TRANSACTIONS_FILE, index=False)
    print(f"Saved {len(transactions_df)} transaction records to {TRANSACTIONS_FILE}")
    
    # Calculate sizes
    accounts_size = os.path.getsize(ACCOUNTS_FILE) / (1024 * 1024)  # Size in MB
    transactions_size = os.path.getsize(TRANSACTIONS_FILE) / (1024 * 1024)  # Size in MB
    total_size = accounts_size + transactions_size
    
    print(f"Total data size: {total_size:.2f} MB (Accounts: {accounts_size:.2f} MB, Transactions: {transactions_size:.2f} MB)")
    
    return synthetic_accounts, transactions_df

if __name__ == "__main__":
    print("Starting synthetic healthcare financial data generation...")
    accounts, transactions = generate_synthetic_data()
    print(f"Data generation complete:")
    print(f"- Generated {len(accounts)} account records")
    print(f"- Generated {len(transactions)} transaction records")
    print(f"- Created detailed product and plan information")
    print("\nSample account record:")
    print(accounts.iloc[0].to_dict()) 