from .notifier_agent import NotifierAgent

def generate_notification(input_json: str) -> str:
    """
    Generate a human-readable notification from Advisor JSON output.
    
    Args:
        input_json: JSON string from Advisor Agent
            
    Returns:
        Formatted notification string
    """
    notifier = NotifierAgent()
    return notifier.generate_notification(input_json)

# For backward compatibility
generate = generate_notification