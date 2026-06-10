import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.advisor.interface import generate_advice
import json

def test_advisor():
    """Test the Advisor Agent implementation."""
    # First, collect and analyze some data
    sample_analysis = {
        "total_wealth": 6574.5,
        "category_breakdown": {
            "food": 150.0,
            "gas": 75.5,
            "rent": 200.0,
            "entertainment": 0.0,
            "subscriptions": 0.0
        },
        "anomalies": [
            {
                "transaction_id": "T001",
                "reason": "Gas expense is 2.5x the category average"
            }
        ],
        "trends": {
            "jan_2023": 2575.5,
            "feb_2023": 0.0,
            "mar_2023": 0.0
        }
    }
    
    # Generate advice based on the analysis
    result = generate_advice(json.dumps(sample_analysis))
    print("Advice result:")
    print(result)

if __name__ == "__main__":
    test_advisor()