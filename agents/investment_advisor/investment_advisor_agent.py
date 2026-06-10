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

class InvestmentAdvisorAgent:
    """Investment Advisor Agent for generating investment strategy recommendations."""
    
    def __init__(self):
        """Initialize the Investment Advisor Agent with LLM capabilities."""
        logger.info("InvestmentAdvisorAgent initialized")
        self.config_manager = LLMConfigManager("llm_config.json")
        self.factory = LLMProviderFactory()
        
        # Log LLM configuration on startup
        self._log_llm_config("investment")
    
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
                logger.info("Investment Advisor LLM Config:")
                logger.info("Enabled: True")
                logger.info(f"Provider: {provider}")
                logger.info(f"Model: {model}")
            else:
                logger.info("Investment Advisor LLM Config:")
                logger.info("Enabled: False")
                logger.info("Reason: NVIDIA_NIM_API_KEY not found")
                logger.info("Using Rule-Based Mode")
        except Exception as e:
            logger.info("Investment Advisor LLM Config:")
            logger.info("Enabled: False")
            logger.info(f"Reason: {str(e)}")
            logger.info("Using Rule-Based Mode")
    
    def generate_investment_advice(self, input_json: str) -> str:
        """
        Generate investment advice based on analysis data.
        
        Args:
            input_json: JSON string from Analyzer Agent
            
        Returns:
            JSON string containing investment advice
        """
        logger.info("Starting investment advice generation")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            # Return default structure on error
            return self._create_default_output()
        
        # Extract data for investment advice generation
        total_wealth = input_data.get("total_wealth", 0.0)
        category_breakdown = input_data.get("category_breakdown", {})
        anomalies = input_data.get("anomalies", [])
        trends = input_data.get("trends", {})
        
        logger.info("Extracted data for investment advice generation")
        
        # Generate investment recommendations based on analysis data
        investment_data = self._generate_investment_advice(total_wealth, category_breakdown, anomalies, trends)
        logger.info("Investment advice generated")
        
        # Create output structure
        output = {
            "advisor_type": "investment",
            "summary": investment_data["summary"],
            "allocation_suggestions": investment_data["allocation_suggestions"],
            "market_outlook": investment_data["market_outlook"],
            "opportunities": investment_data["opportunities"],
            "metadata": {
                "advice_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Store the recommendation in memory
        memory_service.save_memory("investment", "recommendation", output)
        
        logger.info("Investment advice generation completed")
        return json.dumps(output)
    
    def _generate_investment_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                           anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate investment advice based on financial data.
        """
        logger.info("Generating investment advice")
        
        # Try to use LLM if configured
        try:
            # Check if LLM is configured
            config = self.config_manager.get_model_config("investment")
            provider_name = config.get("provider", "litellm")
            model_name = config.get("model", "claude-2")
            
            # Try to create LLM instance
            llm_instance = self.factory.create_llm_instance("investment", self.config_manager)
            
            if llm_instance:
                logger.info(f"Using LLM mode with provider: {provider_name}, model: {model_name}")
                
                # Create prompt for LLM
                prompt = self._create_investment_prompt(total_wealth, category_breakdown, anomalies, trends)
                
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
                        return self._generate_rule_based_investment_advice(total_wealth, category_breakdown, anomalies, trends)
                except Exception as e:
                    logger.warning(f"LLM call failed: {str(e)}. Using rule-based fallback.")
                    return self._generate_rule_based_investment_advice(total_wealth, category_breakdown, anomalies, trends)
            else:
                logger.info("No LLM configured. Using rule-based fallback.")
                return self._generate_rule_based_investment_advice(total_wealth, category_breakdown, anomalies, trends)
        except Exception as e:
            logger.info(f"LLM configuration error: {str(e)}. Using rule-based fallback.")
            return self._generate_rule_based_investment_advice(total_wealth, category_breakdown, anomalies, trends)
    
    def _generate_rule_based_investment_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                                     anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate investment advice using rule-based logic (original implementation).
        """
        logger.info("Generating rule-based investment advice")
        
        # Generate summary based on total wealth
        if total_wealth > 5000:
            summary = "Strong financial position with significant assets for investment opportunities."
        elif total_wealth > 2000:
            summary = "Stable financial position with good potential for investment growth."
        else:
            summary = "Limited investment opportunities with current asset levels."
        
        # Generate allocation suggestions based on wealth level
        allocation_suggestions = [
            "60% stocks, 30% bonds, 10% cash"
        ]
        
        # Generate market outlook
        market_outlook = "Positive for diversified portfolio"
        
        # Generate opportunities
        opportunities = [
            "Consider REITs for diversification",
            "Explore index funds for long-term growth",
            "Evaluate cryptocurrency exposure based on risk tolerance"
        ]
        
        return {
            "summary": summary,
            "allocation_suggestions": allocation_suggestions,
            "market_outlook": market_outlook,
            "opportunities": opportunities
        }
    
    def _create_investment_prompt(self, total_wealth: float, category_breakdown: Dict[str, float], 
                          anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> str:
        """
        Create a prompt for the LLM with financial data.
        """
        prompt = f"""You are an autonomous Investment Advisor Agent operating within a multi-agent financial intelligence platform. Your role is to analyze financial data and provide personalized investment strategy recommendations.

Analyze the provided financial data and generate:
1. A brief summary of the investment position
2. Allocation suggestions
3. Market outlook
4. Opportunities

Financial Data:
- Total Wealth: ${total_wealth:,.2f}
- Spending Categories: {category_breakdown}
- Anomalies: {anomalies}
- Trends: {trends}

Instructions:
- Provide a concise investment position summary
- Generate allocation suggestions
- Provide market outlook
- List opportunities
- Do not include any formatting or markdown
- Respond only with the content for summary, allocation_suggestions, market_outlook, and opportunities fields

Respond with JSON format:
{{
    "summary": "Brief summary of the investment position",
    "allocation_suggestions": [
        "Allocation suggestion 1"
    ],
    "market_outlook": "Market outlook description",
    "opportunities": [
        "Opportunity 1",
        "Opportunity 2"
    ]
}}"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract investment strategy information.
        """
        try:
            # Log the raw response for debugging
            logger.debug(f"Raw LLM Response: {response}")
            
            # Try to parse as JSON
            parsed = json.loads(response)
            
            # Validate that we have the required fields
            required_fields = ["summary", "allocation_suggestions", "market_outlook", "opportunities"]
            if all(field in parsed for field in required_fields):
                logger.info("Successfully parsed LLM response")
                return parsed
            else:
                logger.warning("LLM response missing required fields, falling back to rule-based mode")
                logger.debug(f"Parsed response: {parsed}")
                return None
        except json.JSONDecodeError as e:
            logger.warning(f"JSON parsing failed: {str(e)}, falling back to rule-based mode")
            logger.debug(f"Raw response that failed to parse: {response}")
            return None
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            return None
    
    def _create_default_output(self) -> str:
        """Create a default output structure if advice generation fails."""
        logger.info("Creating default output structure")
        default_output = {
            "advisor_type": "investment",
            "summary": "Unable to generate investment advice due to data issues.",
            "allocation_suggestions": [
                "Ensure proper data input from previous agents.",
                "Check data validation from Analyzer Agent."
            ],
            "market_outlook": "Data validation issues detected",
            "opportunities": [
                "Contact system administrator if issue persists."
            ]
        }
        return json.dumps(default_output)

def main():
    """Main function to demonstrate the Investment Advisor Agent."""
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
    
    advisor = InvestmentAdvisorAgent()
    result = advisor.generate_investment_advice(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()