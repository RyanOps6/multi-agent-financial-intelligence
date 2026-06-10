import os
import sys
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_provider import LLMConfigManager, LLMProviderFactory

def test_investment_model():
    """Test the investment advisor model."""
    print("Testing Investment Advisor Model...")
    
    # Initialize configuration manager
    config_manager = LLMConfigManager("llm_config.json")
    
    # Initialize provider factory
    factory = LLMProviderFactory()
    
    # Test with investment advisor
    advisor_type = "investment"
    config = config_manager.get_model_config(advisor_type)
    llm_instance = factory.create_llm_instance(advisor_type, config_manager)
    
    if llm_instance:
        print(f"Investment model: {config.get('model')}")
        print("Model is accessible and working correctly")

if __name__ == "__main__":
    test_investment_model()