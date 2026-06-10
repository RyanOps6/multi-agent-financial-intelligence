import json
from typing import Dict, Any
from .advisor_agent import AdvisorAgent

def generate_financial_advice(input_json: str) -> str:
    """
    Generate financial advice using the Advisor Agent.
    
    Args:
        input_json: JSON string from Analyzer Agent
            
    Returns:
        JSON string containing advice and recommendations
    """
    advisor = AdvisorAgent()
    return advisor.generate_advice(input_json)

# For backward compatibility
generate_advice = generate_financial_advice
