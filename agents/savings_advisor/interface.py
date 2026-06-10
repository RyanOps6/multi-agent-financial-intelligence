from .savings_advisor_agent import SavingsAdvisorAgent

def generate_savings_advice(input_json: str):
    """
    Generate savings advice using the Savings Advisor Agent.
    
    Args:
        input_json: JSON string from Analyzer Agent
            
    Returns:
        JSON string containing savings advice
    """
    advisor = SavingsAdvisorAgent()
    return advisor.generate_savings_advice(input_json)

# For backward compatibility
generate_advice = generate_savings_advice