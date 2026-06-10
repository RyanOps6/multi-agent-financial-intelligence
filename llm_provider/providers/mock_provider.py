from typing import Dict, Any
from ..interface import LLMInterface, LLMProvider


class MockLLMInterface(LLMInterface):
    """Mock LLM implementation for testing."""
    
    def __init__(self, model_name: str = "mock-model"):
        """Initialize the mock LLM interface.
        
        Args:
            model_name: The model name to use
        """
        self.model_name = model_name
        self.model_info = {
            "model": model_name,
            "provider": "mock"
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a mock response.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters
            
        Returns:
            A mock response
        """
        return f"Mock response for: {prompt}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get mock model information.
        
        Returns:
            Dictionary containing model information
        """
        return self.model_info


class MockLLMProvider(LLMProvider):
    """Mock provider for testing."""
    
    def get_provider_name(self) -> str:
        return "mock"
    
    def is_available(self) -> bool:
        """Check if the provider is available.
        
        Returns:
            True if available, False otherwise
        """
        return True
    
    def load_model(self, model_config: Dict[str, Any]) -> LLMInterface:
        """Load a model with the specified configuration.
        
        Args:
            model_config: Configuration for the model
            
        Returns:
            An instance of the LLM interface
        """
        return MockLLMInterface(model_name=model_config.get("model", "mock-model"))