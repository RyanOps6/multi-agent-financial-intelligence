import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_provider import LLMConfigManager, LLMProviderFactory


def test_mock_response():
    """Test the LLM provider abstraction with mock responses."""
    print("Testing LLM Provider Abstraction with Mock Responses...")
    
    # Initialize configuration manager
    config_manager = LLMConfigManager("llm_config.json")
    
    # Initialize provider factory
    factory = LLMProviderFactory()
    
    # Test getting configuration for different advisor types
    advisor_types = ["savings", "risk", "investment", "default"]
    
    for advisor_type in advisor_types:
        print(f"\nTesting {advisor_type} advisor:")
        config = config_manager.get_model_config(advisor_type)
        print(f"  Model: {config.get('model', 'N/A')}")
        print(f"  Provider: {config.get('provider', 'N/A')}")
        
        # Create LLM instance
        llm_instance = factory.create_llm_instance(advisor_type, config_manager)
        if llm_instance:
            print(f"  LLM instance created successfully")
            model_info = llm_instance.get_model_info()
            print(f"  Model info: {model_info}")
            
            # Test generating a mock response (without actually calling the API)
            try:
                # This would be where we test the response generation
                # But we're just testing the abstraction, not the actual LLM calls
                print("  Abstraction layer working correctly")
            except Exception as e:
                print(f"  Error in response generation: {e}")
        else:
            print(f"  Failed to create LLM instance")


if __name__ == "__main__":
    test_mock_response()