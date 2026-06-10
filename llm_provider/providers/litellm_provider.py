import importlib
from typing import Dict, Any
from ..interface import LLMInterface, LLMProvider


# Check if LiteLLM is available
try:
    import litellm
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False


class LiteLLMInterface(LLMInterface):
    """LiteLLM implementation of the LLM interface."""
    
    def __init__(self, model_name: str = "gpt-3.5-turbo"):
        """Initialize the LiteLLM interface.
        
        Args:
            model_name: The model to use for generation
        """
        self.model_name = model_name
        self.model_info = {
            "model": model_name,
            "provider": "litellm"
        }
    
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response using LiteLLM.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters for the LLM call
            
        Returns:
            The generated response as a string
        """
        import litellm
        import os
        # Use environment variable for API key if needed
        api_key = os.getenv("NVIDIA_NIM_API_KEY", "")
        if not api_key:
            api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Prepare the messages
        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        # Call the model
        response = litellm.completion(
            model=self.model_name,
            messages=messages,
            **kwargs
        )
        
        return response.choices[0].message.content
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model.
        
        Returns:
            Dictionary containing model information
        """
        return self.model_info


class LiteLLMProvider(LLMProvider):
    """Provider implementation for LiteLLM."""
    
    def get_provider_name(self) -> str:
        return "litellm"
    
    def is_available(self):
        """Check if the provider is available."""
        try:
            import litellm
            return True
        except ImportError:
            return False
    
    def load_model(self, model_config: Dict[str, Any]) -> LLMInterface:
        """Load a model with the specified configuration.
        
        Args:
            model_config: Configuration for the model
            
        Returns:
            An instance of the LLM interface
        """
        return LiteLLMInterface(model_name=model_config.get("model", "gpt-3.5-turbo"))


# For the advisors
llm_interface = LiteLLMInterface()
llm_interface = llm_interface  # This will be used by the advisors