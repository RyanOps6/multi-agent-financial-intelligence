import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.advisor.interface import generate_advice
from agents.notifier.interface import generate_notification

import json

def test_notifier():
    """Test the Notifier Agent implementation."""
    # First, collect and analyze some data
    sample_analysis = {
        "summary": "Your financial position is strong with a total wealth of $6,574.50.",
        "recommendations": [
            "Consider setting aside 20% of income for savings to build long-term wealth.",
            "Review your spending on categories that exceed budgeted amounts.",
            "Diversify your investments to reduce risk exposure.",
            "Set up automatic transfers to savings to ensure consistent saving habits."
        ],
        "risk_alerts": [
            "Unusual spending patterns detected that are significantly above category averages.",
            "Monitor spending trends to identify potential savings opportunities."
        ]
    }
    
    # Generate notification based on the analysis
    result = generate_notification(json.dumps(sample_analysis))
    print("Notification result:")
    print(result)

if __name__ == "__main__":
    import json
    test_notifier()
