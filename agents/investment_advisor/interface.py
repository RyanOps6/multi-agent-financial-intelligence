from .investment_advisor_agent import InvestmentAdvisorAgent

def generate_investment_advice(input_json: str):
    """
    Generate investment advice using the Investment Advisor Agent.
    
    Args:
        input_json: JSON string from Analyzer Agent
            
    Returns:
        JSON string containing investment advice
    """
    advisor = InvestmentAdvisorAgent()
    return advisor.generate_investment_advice(input_json)

# For backward compatibility
generate_advice = generate_investment_advice