#!/usr/bin/env python
# src/financial_researcher/main.py
import sys
import warnings
from datetime import datetime
from financial_researcher.crew import FinancialResearcher
 
# Create output directory if it doesn't exist
 
def run():
    """
    Run the financial research crew.
    """
    inputs = {
        'company': 'Tesla'
    }
 
    result = FinancialResearcher().crew().kickoff(inputs=inputs)
    print(result.raw)
 
if __name__ == "__main__":
    run()