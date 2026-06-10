from typing import Dict, Any, Optional
from .interface import LLMProvider, LLMInterface
from .config import LLMConfigManager
from .providers.mock_provider import MockLLMProvider, MockLLMInterface

class LLMProviderFactory:
    """Factory for creating LLM provider instances."""
    
    def __init__(self):
        """Initialize the provider factory."""
        self._providers = {}
        self._register_default_providers()
    
    def _register_default_providers(self):
        """Register default providers."""
        # Register the LiteLLM provider as default
        try:
            from .providers.litellm_provider import LiteLLMProvider
            self.register_provider("litellm", LiteLLMProvider())
        except ImportError:
            # If LiteLLM is not available, register a mock provider
            self.register_provider("litellm", MockLLMProvider())
    
    def register_provider(self, name: str, provider: LLMProvider):
        """Register a provider with the factory.
        
        Args:
            name: Name of the provider
            provider: Provider instance
        """
        self._providers[name] = provider
    
    def get_provider(self, name: str) -> Optional[LLMProvider]:
        """Get a registered provider by name.
        
        Args:
            name: Name of the provider
            
        Returns:
            Provider instance or None if not found
        """
        return self._providers.get(name)
    
    def create_llm_instance(self, advisor_type: str, config_manager: LLMConfigManager) -> Optional[LLMInterface]:
        """Create an LLM instance for a specific advisor type.
        
        Args:
            advisor_type: Type of advisor
            config_manager: Configuration manager instance
            
        Returns:
            LLM interface instance or None if creation fails
        """
        # Get configuration for the advisor type
        model_config = config_manager.get_model_config(advisor_type)
        provider_name = model_config.get("provider", "litellm")
        
        # Get the provider
        provider = self._providers.get(provider_name)
        if not provider:
            # Try to load a default provider if the specified one is not available
            provider = self._providers.get("litellm")
            if not provider:
                return None
        
        # Check if provider is available
        if not provider.is_available():
            return None
            
        # Load the model
        try:
            return provider.load_model(model_config)
        except Exception:
            return None