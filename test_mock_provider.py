import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_provider.providers.mock_provider import MockLLMProvider
from llm_provider import LLMConfigManager, LLMProviderFactory

def test_mock_provider():
    """Test the mock provider."""
    print("Testing Mock Provider...")
    
    # Initialize provider factory
    factory = LLMProviderFactory()
    
    # Test creating LLM instances with mock provider
    mock_provider = MockLLMProvider()
    factory.register_provider("mock", mock_provider)
    
    # Test getting configuration
    config_manager = LLMConfigManager("llm_config.json")
    
    # Test creating LLM instances
    print("\nTesting LLM instance creation with mock provider:")
    for advisor_type in ["savings", "risk", "investment", "default"]:
        llm_instance = factory.create_llm_instance(advisor_type, config_manager)
        if llm_instance:
            print(f"  {advisor_type.capitalize()} advisor LLM instance created successfully")
            response = llm_instance.generate_response("Test prompt")
            print(f"    Response: {response}")
        else:
            print(f"  Failed to create LLM instance for {advisor_type} advisor")

if __name__ == "__main__":
    test_mock_provider()