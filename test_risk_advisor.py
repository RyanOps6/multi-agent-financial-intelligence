import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.risk_advisor.interface import generate_risk_advice
import json

def test_risk_advisor():
    """Test the Risk Advisor Agent implementation."""
    # Sample analysis data
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
    result = generate_risk_advice(json.dumps(sample_analysis))
    print("Risk Advisor result:")
    print(result)

if __name__ == "__main__":
    test_risk_advisor()