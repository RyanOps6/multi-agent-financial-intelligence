import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvisorAgent:
    """Advisor Agent for generating financial advice using LLM."""
    
    def __init__(self):
        """Initialize the Advisor Agent."""
        logger.info("AdvisorAgent initialized")
    
    def generate_advice(self, input_json: str) -> str:
        """
        Generate financial advice using LLM based on analysis data.
        
        Args:
            input_json: JSON string from Analyzer Agent
            
        Returns:
            JSON string containing advice and recommendations
        """
        logger.info("Starting advice generation")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            # Return default structure on error
            return self._create_default_output()
        
        # Validate input data
        if not self._validate_input(input_data):
            logger.warning("Input validation failed, using default values")
            input_data = self._create_default_input()
        
        logger.info("Input data validated")
        
        # Extract data for advice generation
        total_wealth = input_data.get("total_wealth", 0.0)
        category_breakdown = input_data.get("category_breakdown", {})
        anomalies = input_data.get("anomalies", [])
        trends = input_data.get("trends", {})
        
        logger.info("Extracted data for advice generation")
        
        # Generate advice using LLM (mocked implementation)
        advice_data = self._generate_llm_advice(total_wealth, category_breakdown, anomalies, trends)
        logger.info("Advice generated using LLM")
        
        # Create output structure
        output = {
            "summary": advice_data["summary"],
            "recommendations": advice_data["recommendations"],
            "risk_alerts": advice_data["risk_alerts"],
            "metadata": {
                "advice_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        logger.info("Advice generation completed")
        return json.dumps(output)
    
    def _validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input JSON structure."""
        logger.info("Validating input data")
        
        # In a real implementation, this would check for required fields
        # For now, we'll just return True to process all inputs
        return True
    
    def _create_default_input(self) -> Dict[str, Any]:
        """Create a default input structure if validation fails."""
        logger.info("Creating default input structure")
        return {
            "total_wealth": 0.0,
            "category_breakdown": {},
            "anomalies": [],
            "trends": {}
        }
    
    def _create_default_output(self) -> str:
        """Create a default output structure if advice generation fails."""
        logger.info("Creating default output structure")
        default_output = {
            "summary": "Unable to generate advice due to data issues.",
            "recommendations": [
                "Ensure proper data input from previous agents.",
                "Check data validation from Analyzer Agent.",
                "Contact system administrator if issue persists."
            ],
            "risk_alerts": [
                "Data validation failed in Advisor Agent."
            ]
        }
        return json.dumps(default_output)
    
    def _generate_llm_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                           anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate advice using LLM (mocked implementation).
        
        In a real implementation, this would connect to an LLM API like NVIDIA or LiteLLM.
        """
        logger.info("Generating advice with LLM")
        
        # This is a mocked implementation that simulates LLM responses
        # In a real implementation, this would call an actual LLM API
        
        # Generate summary based on total wealth
        if total_wealth > 5000:
            summary = f"Your financial position is strong with a total wealth of ${total_wealth:,.2f}."
        elif total_wealth > 2000:
            summary = f"Your financial position is stable with a total wealth of ${total_wealth:,.2f}."
        else:
            summary = f"Your financial position requires attention with a total wealth of ${total_wealth:,.2f}."
        
        # Generate recommendations based on category breakdown and anomalies
        recommendations = [
            "Consider setting aside 20% of income for savings to build long-term wealth.",
            "Review your spending on categories that exceed budgeted amounts.",
            "Diversify your investments to reduce risk exposure.",
            "Set up automatic transfers to savings to ensure consistent saving habits."
        ]
        
        # Generate risk alerts based on anomalies and trends
        risk_alerts = []
        if anomalies:
            risk_alerts.append("Unusual spending patterns detected that are significantly above category averages.")
        
        if not risk_alerts:
            risk_alerts.append("No significant risks detected at this time.")
        
        # Add more alerts based on trends
        risk_alerts.append("Monitor spending trends to identify potential savings opportunities.")
        
        return {
            "summary": summary,
            "recommendations": recommendations,
            "risk_alerts": risk_alerts
        }

def main():
    """Main function to demonstrate the Advisor Agent."""
    # Example usage with sample data
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
    
    advisor = AdvisorAgent()
    result = advisor.generate_advice(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()