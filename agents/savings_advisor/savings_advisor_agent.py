import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from memory_service import memory_service

# LLM Provider imports
from llm_provider import LLMConfigManager, LLMProviderFactory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SavingsAdvisorAgent:
    """Savings Advisor Agent for generating savings optimization recommendations."""
    
    def __init__(self):
        """Initialize the Savings Advisor Agent with LLM capabilities."""
        logger.info("SavingsAdvisorAgent initialized")
        self.config_manager = LLMConfigManager("llm_config.json")
        self.factory = LLMProviderFactory()
        
        # Log LLM configuration on startup
        self._log_llm_config("savings")
    
    def _log_llm_config(self, advisor_type: str):
        """Log LLM configuration for startup information."""
        try:
            config = self.config_manager.get_model_config(advisor_type)
            provider = config.get("provider", "litellm")
            model = config.get("model", "unknown")
            
            # Check if API key is available
            import os
            nvidia_api_key = os.getenv("NVIDIA_NIM_API_KEY", "")
            
            if nvidia_api_key:
                logger.info("Savings Advisor LLM Config:")
                logger.info("Enabled: True")
                logger.info(f"Provider: {provider}")
                logger.info(f"Model: {model}")
            else:
                logger.info("Savings Advisor LLM Config:")
                logger.info("Enabled: False")
                logger.info("Reason: NVIDIA_NIM_API_KEY not found")
                logger.info("Using Rule-Based Mode")
        except Exception as e:
            logger.info("Savings Advisor LLM Config:")
            logger.info("Enabled: False")
            logger.info(f"Reason: {str(e)}")
            logger.info("Using Rule-Based Mode")
    
    def generate_savings_advice(self, input_json: str) -> str:
        """
        Generate savings advice based on analysis data.
        
        Args:
            input_json: JSON string from Analyzer Agent
            
        Returns:
            JSON string containing savings advice
        """
        logger.info("Starting savings advice generation")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            # Return default structure on error
            return self._create_default_output()
        
        # Extract data for savings advice generation
        total_wealth = input_data.get("total_wealth", 0.0)
        category_breakdown = input_data.get("category_breakdown", {})
        anomalies = input_data.get("anomalies", [])
        trends = input_data.get("trends", {})
        
        logger.info("Extracted data for savings advice generation")
        
        # Generate savings recommendations based on analysis data
        savings_data = self._generate_savings_advice(total_wealth, category_breakdown, anomalies, trends)
        logger.info("Savings advice generated")
        
        # Create output structure
        output = {
            "advisor_type": "savings",
            "summary": savings_data["summary"],
            "recommendations": savings_data["recommendations"],
            "potential_savings": savings_data["potential_savings"],
            "metadata": {
                "advice_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Store the recommendation in memory
        memory_service.save_memory("savings", "recommendation", output)
        
        logger.info("Savings advice generation completed")
        return json.dumps(output)
    
    def _generate_savings_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                           anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate savings advice based on financial data.
        """
        logger.info("Generating savings advice")
        
        # Try to use LLM if configured
        try:
            # Check if LLM is configured
            config = self.config_manager.get_model_config("savings")
            provider_name = config.get("provider", "litellm")
            model_name = config.get("model", "gpt-3.5-turbo")
            
            # Try to create LLM instance
            llm_instance = self.factory.create_llm_instance("savings", self.config_manager)
            
            if llm_instance:
                logger.info(f"Using LLM mode with provider: {provider_name}, model: {model_name}")
                
                # Create prompt for LLM
                prompt = self._create_savings_prompt(total_wealth, category_breakdown, anomalies, trends)
                
                # Try to get LLM response
                try:
                    llm_response = llm_instance.generate_response(prompt)
                    logger.info("LLM call successful")
                    
                    # Parse LLM response
                    parsed_response = self._parse_llm_response(llm_response)
                    if parsed_response:
                        return parsed_response
                    else:
                        logger.warning("Failed to parse LLM response, using rule-based fallback")
                        return self._generate_rule_based_savings_advice(total_wealth, category_breakdown, anomalies, trends)
                except Exception as e:
                    logger.warning(f"LLM call failed: {str(e)}. Using rule-based fallback.")
                    return self._generate_rule_based_savings_advice(total_wealth, category_breakdown, anomalies, trends)
            else:
                logger.info("No LLM configured. Using rule-based fallback.")
                return self._generate_rule_based_savings_advice(total_wealth, category_breakdown, anomalies, trends)
        except Exception as e:
            logger.info(f"LLM configuration error: {str(e)}. Using rule-based fallback.")
            return self._generate_rule_based_savings_advice(total_wealth, category_breakdown, anomalies, trends)
    
    def _generate_rule_based_savings_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                                     anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate savings advice using rule-based logic (original implementation).
        """
        logger.info("Generating rule-based savings advice")
        
        # Generate summary based on total wealth
        if total_wealth > 5000:
            summary = "Your financial position is strong with significant wealth for savings optimization."
        elif total_wealth > 2000:
            summary = "Your financial position is stable with good potential for savings growth."
        else:
            summary = "Your financial position requires attention to build better savings habits."
        
        # Generate recommendations based on category breakdown and anomalies
        recommendations = [
            "Set aside 20% of monthly income for savings to build long-term wealth.",
            "Review spending on categories that exceed budgeted amounts to identify savings opportunities.",
            "Create an emergency fund with 3-6 months of expenses.",
            "Consider automating transfers to savings accounts to ensure consistent saving habits."
        ]
        
        # Calculate potential savings based on analysis
        potential_savings = 0.0
        if category_breakdown:
            # Simple calculation based on total spending
            total_spending = sum(category_breakdown.values())
            potential_savings = total_spending * 0.15  # Assume 15% potential savings
        
        return {
            "summary": summary,
            "recommendations": recommendations,
            "potential_savings": potential_savings
        }
    
    def _create_savings_prompt(self, total_wealth: float, category_breakdown: Dict[str, float], 
                          anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> str:
        """
        Create a prompt for the LLM with financial data.
        """
        prompt = f"""You are an autonomous Savings Advisor Agent operating within a multi-agent financial intelligence platform. Your role is to analyze financial data and provide personalized savings recommendations.

Analyze the provided financial data and generate:
1. A brief summary of the financial position (2-3 sentences)
2. 4 specific savings recommendations based on the data
3. Estimated potential savings amount based on the analysis

Financial Data:
- Total Wealth: ${total_wealth:,.2f}
- Spending Categories: {category_breakdown}
- Anomalies: {anomalies}
- Trends: {trends}

Instructions:
- Provide a concise analysis summary
- Generate 4 specific, actionable savings recommendations
- Focus on data-driven insights
- Do not include any formatting or markdown
- Respond only with the content for summary and recommendations fields

Respond with JSON format:
{{
    "summary": "Brief summary of the financial position",
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2",
        "Recommendation 3",
        "Recommendation 4"
    ],
    "potential_savings": 0.0
}}"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract summary and recommendations.
        """
        try:
            # Log the raw response for debugging
            logger.debug(f"Raw LLM Response: {response}")
            
            # Try to parse as JSON
            parsed = json.loads(response)
            
            # Validate that we have the required fields
            if "summary" in parsed and "recommendations" in parsed:
                logger.info("Successfully parsed LLM response")
                
                # Add potential_savings if not present
                if "potential_savings" not in parsed:
                    parsed["potential_savings"] = 0.0
                return parsed
            else:
                return None
        except Exception as e:
            logger.warning("Error parsing LLM response: %s", exc_info=e)
            return None
    
    def _create_default_output(self) -> str:
        """Create a default output structure if advice generation fails."""
        logger.info("Creating default output structure")
        default_output = {
            "advisor_type": "savings",
            "summary": "Unable to generate savings advice due to data issues.",
            "recommendations": [
                "Ensure proper data input from previous agents.",
                "Check data validation from Analyzer Agent."
            ],
            "potential_savings": 0.0
        }
        return json.dumps(default_output)

def main():
    """Main function to demonstrate the Savings Advisor Agent."""
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
    
    advisor = SavingsAdvisorAgent()
    result = advisor.generate_savings_advice(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()