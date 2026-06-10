from .risk_advisor_agent import RiskAdvisorAgent

def generate_risk_advice(input_json: str):
    """
    Generate risk advice using the Risk Advisor Agent.
    
    Args:
        input_json: JSON string from Analyzer Agent
            
    Returns:
        JSON string containing risk advice
    """
    advisor = RiskAdvisorAgent()
    return advisor.generate_risk_advice(input_json)

# For backward compatibility
generate_advice = generate_risk_advice