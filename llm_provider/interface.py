from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json


class LLMInterface(ABC):
    """Abstract base class for LLM providers."""
    
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM.
        
        Args:
            prompt: The input prompt for the LLM
            **kwargs: Additional parameters for the LLM
            
        Returns:
            The generated response as a string
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model.
        
        Returns:
            Dictionary containing model information
        """
        pass


class LLMProvider(ABC):
    """Abstract base class for LLM provider implementations."""
    
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider.
        
        Returns:
            Name of the provider
        """
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available.
        
        Returns:
            True if the provider is available, False otherwise
        """
        pass
    
    @abstractmethod
    def load_model(self, model_config: Dict[str, Any]) -> LLMInterface:
        """Load a model with the specified configuration.
        
        Args:
            model_config: Configuration for the model
            
        Returns:
            An instance of the LLM interface
        """
        pass