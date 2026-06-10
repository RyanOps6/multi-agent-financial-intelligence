import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from llm_provider import LLMConfigManager, LLMProviderFactory


def test_llm_provider():
    """Test the LLM provider abstraction."""
    print("Testing LLM Provider Abstraction...")
    
    # Initialize configuration manager
    config_manager = LLMConfigManager("llm_config.json")
    
    # Initialize provider factory
    factory = LLMProviderFactory()
    
    # Test getting configuration for different advisor types
    advisor_types = ["savings", "risk", "investment", "default"]
    
    for advisor_type in advisor_types:
        print(f"\nTesting {advisor_type} advisor configuration:")
        config = config_manager.get_model_config(advisor_type)
        print(f"  Model: {config.get('model', 'N/A')}")
        print(f"  Provider: {config.get('provider', 'N/A')}")
        print(f"  Parameters: {config.get('parameters', {})}")
    
    # Test creating LLM instances
    print("\nTesting LLM instance creation:")
    for advisor_type in advisor_types:
        llm_instance = factory.create_llm_instance(advisor_type, config_manager)
        if llm_instance:
            print(f"  {advisor_type.capitalize()} advisor LLM instance created successfully")
            model_info = llm_instance.get_model_info()
            print(f"    Model info: {model_info}")
        else:
            print(f"  Failed to create LLM instance for {advisor_type} advisor")


if __name__ == "__main__":
    test_llm_provider()