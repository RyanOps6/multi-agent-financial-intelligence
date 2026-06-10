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

class RiskAdvisorAgent:
    """Risk Advisor Agent for generating risk assessment recommendations."""
    
    def __init__(self):
        """Initialize the Risk Advisor Agent with LLM capabilities."""
        logger.info("RiskAdvisorAgent initialized")
        self.config_manager = LLMConfigManager("llm_config.json")
        self.factory = LLMProviderFactory()
        
        # Log LLM configuration on startup
        self._log_llm_config("risk")
    
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
                logger.info("Risk Advisor LLM Config:")
                logger.info("Enabled: True")
                logger.info(f"Provider: {provider}")
                logger.info(f"Model: {model}")
            else:
                logger.info("Risk Advisor LLM Config:")
                logger.info("Enabled: False")
                logger.info("Reason: NVIDIA_NIM_API_KEY not found")
                logger.info("Using Rule-Based Mode")
        except Exception as e:
            logger.info("Risk Advisor LLM Config:")
            logger.info("Enabled: False")
            logger.info(f"Reason: {str(e)}")
            logger.info("Using Rule-Based Mode")
    
    def generate_risk_advice(self, input_json: str) -> str:
        """
        Generate risk advice based on analysis data.
        
        Args:
            input_json: JSON string from Analyzer Agent
            
        Returns:
            JSON string containing risk advice
        """
        logger.info("Starting risk advice generation")
        
        try:
            # Parse input JSON
            input_data = json.loads(input_json)
            logger.info("Input JSON parsed successfully")
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing input JSON: {str(e)}")
            # Return default structure on error
            return self._create_default_output()
        
        # Extract data for risk advice generation
        total_wealth = input_data.get("total_wealth", 0.0)
        category_breakdown = input_data.get("category_breakdown", {})
        anomalies = input_data.get("anomalies", [])
        trends = input_data.get("trends", {})
        
        logger.info("Extracted data for risk advice generation")
        
        # Generate risk recommendations based on analysis data
        risk_data = self._generate_risk_advice(total_wealth, category_breakdown, anomalies, trends)
        logger.info("Risk advice generated")
        
        # Create output structure
        output = {
            "advisor_type": "risk",
            "summary": risk_data["summary"],
            "risk_score": risk_data["risk_score"],
            "findings": risk_data["findings"],
            "mitigation_strategies": risk_data["mitigation_strategies"],
            "metadata": {
                "advice_timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }
        
        # Store the recommendation in memory
        memory_service.save_memory("risk", "recommendation", output)
        
        logger.info("Risk advice generation completed")
        return json.dumps(output)
    
    def _generate_risk_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                           anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate risk advice based on financial data.
        """
        logger.info("Generating risk advice")
        
        # Try to use LLM if configured
        try:
            # Check if LLM is configured
            config = self.config_manager.get_model_config("risk")
            provider_name = config.get("provider", "litellm")
            model_name = config.get("model", "gpt-3.5-turbo")
            
            # Try to create LLM instance
            llm_instance = self.factory.create_llm_instance("risk", self.config_manager)
            
            if llm_instance:
                logger.info(f"Using LLM mode with provider: {provider_name}, model: {model_name}")
                
                # Create prompt for LLM
                prompt = self._create_risk_prompt(total_wealth, category_breakdown, anomalies, trends)
                
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
                        return self._generate_rule_based_risk_advice(total_wealth, category_breakdown, anomalies, trends)
                except Exception as e:
                    logger.warning(f"LLM call failed: {str(e)}. Using rule-based fallback.")
                    return self._generate_rule_based_risk_advice(total_wealth, category_breakdown, anomalies, trends)
            else:
                logger.info("No LLM configured. Using rule-based fallback.")
                return self._generate_rule_based_risk_advice(total_wealth, category_breakdown, anomalies, trends)
        except Exception as e:
            logger.info(f"LLM configuration error: {str(e)}. Using rule-based fallback.")
            return self._generate_rule_based_risk_advice(total_wealth, category_breakdown, anomalies, trends)
    
    def _generate_rule_based_risk_advice(self, total_wealth: float, category_breakdown: Dict[str, float], 
                                     anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> Dict[str, Any]:
        """
        Generate risk advice using rule-based logic (original implementation).
        """
        logger.info("Generating rule-based risk advice")
        
        # Generate summary based on total wealth and anomalies
        if anomalies:
            summary = "Risk assessment indicates potential financial risks that should be addressed."
        else:
            summary = "Risk assessment shows a relatively stable financial position."
        
        # Calculate risk score based on analysis
        risk_score = 0.5  # Default moderate risk
        if anomalies:
            risk_score = min(1.0, 0.3 + len(anomalies) * 0.2)  # Increase risk based on anomalies
        
        # Generate findings based on analysis
        findings = [
            "Anomalies detected in spending patterns",
            "Volatility in spending categories"
        ]
        
        # Generate mitigation strategies
        mitigation_strategies = [
            "Diversify investment portfolio",
            "Set spending alerts for high-risk categories",
            "Establish emergency fund"
        ]
        
        return {
            "summary": summary,
            "risk_score": risk_score,
            "findings": findings,
            "mitigation_strategies": mitigation_strategies
        }
    
    def _create_risk_prompt(self, total_wealth: float, category_breakdown: Dict[str, float], 
                          anomalies: List[Dict[str, str]], trends: Dict[str, float]) -> str:
        """
        Create a prompt for the LLM with financial data.
        """
        prompt = f"""You are an autonomous Risk Advisor Agent operating within a multi-agent financial intelligence platform. Your role is to analyze financial data and provide personalized risk assessment recommendations.

Analyze the provided financial data and generate:
1. A brief summary of the risk assessment
2. Risk score (0.0-1.0)
3. Key findings
4. Mitigation strategies

Financial Data:
- Total Wealth: ${total_wealth:,.2f}
- Spending Categories: {category_breakdown}
- Anomalies: {anomalies}
- Trends: {trends}

Instructions:
- Provide a concise risk assessment summary
- Generate a risk score between 0.0-1.0
- List key findings
- Provide 3-5 mitigation strategies
- Do not include any formatting or markdown
- Respond only with the content for summary, risk_score, findings, and mitigation_strategies fields

Respond with JSON format:
{{
    "summary": "Brief summary of the risk assessment",
    "risk_score": 0.5,
    "findings": [
        "Finding 1",
        "Finding 2"
    ],
    "mitigation_strategies": [
        "Strategy 1",
        "Strategy 2",
        "Strategy 3"
    ]
}}"""
        return prompt
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse the LLM response to extract risk assessment information.
        """
        try:
            # Log the raw response for debugging
            logger.debug(f"Raw LLM Response: {response}")
            
            # Try to parse as JSON
            parsed = json.loads(response)
            
            # Validate that we have the required fields
            required_fields = ["summary", "risk_score", "findings", "mitigation_strategies"]
            if all(field in parsed for field in required_fields):
                logger.info("Successfully parsed LLM response")
                return parsed
            else:
                logger.warning("LLM response missing required fields, falling back to rule-based mode")
                logger.debug(f"Parsed response: {parsed}")
                return None
        except json.JSONError as e:
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
            "advisor_type": "risk",
            "summary": "Unable to generate risk advice due to data issues.",
            "risk_score": 0.5,
            "findings": [
                "Data validation issues detected"
            ],
            "mitigation_strategies": [
                "Ensure proper data input from previous agents.",
                "Check data validation from Analyzer Agent."
            ]
        }
        return json.dumps(default_output)

def main():
    """Main function to demonstrate the Risk Advisor Agent."""
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
    
    advisor = RiskAdvisorAgent()
    result = advisor.generate_risk_advice(json.dumps(sample_input))
    print(result)

if __name__ == "__main__":
    main()