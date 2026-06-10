import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.savings_advisor.savings_advisor_agent import SavingsAdvisorAgent
from agents.risk_advisor.risk_advisor_agent import RiskAdvisorAgent
from agents.investment_advisor.investment_advisor_agent import InvestmentAdvisorAgent
from memory_service import memory_service

def test_advisor_memory_integration():
    """Test that advisors can store and retrieve memories."""
    
    # Test data
    sample_input = {
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
    
    # Test savings advisor
    print("Testing Savings Advisor...")
    savings_advisor = SavingsAdvisorAgent()
    savings_result = savings_advisor.generate_savings_advice(str(sample_input).replace("'", '"'))
    print("Savings advice generated and stored in memory")
    
    # Test risk advisor
    print("\nTesting Risk Advisor...")
    risk_advisor = RiskAdvisorAgent()
    risk_result = risk_advisor.generate_risk_advice(str(sample_input).replace("'", '"'))
    print("Risk advice generated and stored in memory")
    
    # Test investment advisor
    print("\nTesting Investment Advisor...")
    investment_advisor = InvestmentAdvisorAgent()
    investment_result = investment_advisor.generate_investment_advice(str(sample_input).replace("'", '"'))
    print("Investment advice generated and stored in memory")
    
    # Test retrieving memories
    print("\nRetrieving stored memories...")
    savings_memories = memory_service.retrieve_memories("savings", "recommendation")
    risk_memories = memory_service.retrieve_memories("risk", "recommendation")
    investment_memories = memory_service.retrieve_memories("investment", "recommendation")
    
    print(f"Retrieved {len(savings_memories)} savings memories")
    print(f"Retrieved {len(risk_memories)} risk memories")
    print(f"Retrieved {len(investment_memories)} investment memories")
    
    print("\nMemory integration test completed successfully!")

if __name__ == "__main__":
    test_advisor_memory_integration()