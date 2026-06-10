import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_provider import LLMConfigManager, LLMProviderFactory
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_llm_response():
    """Test the LLM response and parsing."""
    print("Testing LLM Response and Parsing...")
    
    # Initialize configuration manager
    config_manager = LLMConfigManager("llm_config.json")
    
    # Initialize provider factory
    factory = LLMProviderFactory()
    
    # Test data
    sample_data = {
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
    
    # Test with savings advisor
    advisor_type = "savings"
    config = config_manager.get_model_config(advisor_type)
    llm_instance = factory.create_llm_instance(advisor_type, config_manager)
    
    if llm_instance:
        # Create prompt
        prompt = f"""You are an autonomous Savings Advisor Agent operating within a multi-agent financial intelligence platform. Your role is to analyze financial data and provide personalized savings recommendations.

Analyze the provided financial data and generate:
1. A brief summary of the financial position (2-3 sentences)
2. 4 specific savings recommendations based on the data

Financial Data:
- Total Wealth: ${sample_data['total_wealth']:,.2f}
- Spending Categories: {sample_data['category_breakdown']}
- Anomalies: {sample_data['anomalies']}
- Trends: {sample_data['trends']}

Instructions:
- Provide a concise analysis summary
- Generate 4 specific, actionable savings recommendations
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
    ]
}}"""
        
        print("Sending prompt to LLM...")
        try:
            response = llm_instance.generate_response(prompt)
            print(f"Raw LLM Response: {response}")
            
            # Try to parse the response
            try:
                # First, try to parse as JSON
                parsed = json.loads(response)
                print("Parsed JSON successfully!")
                print(f"Parsed Response: {parsed}")
            except json.JSONDecodeError as e:
                print(f"JSON parsing failed: {e}")
                print("Falling back to rule-based mode")
                
        except Exception as e:
            print(f"Error calling LLM: {e}")

if __name__ == "__main__":
    test_llm_response()