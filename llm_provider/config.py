import json
import os
from typing import Dict, Any, Optional


class LLMConfigManager:
    """Configuration manager for LLM providers and models."""
    
    def __init__(self, config_path: str = "llm_config.json"):
        """Initialize the configuration manager.
        
        Args:
            config_path: Path to the configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file.
        
        Returns:
            Configuration dictionary
        """
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Return default configuration if file doesn't exist
            return self._get_default_config()
        except Exception:
            # Return default configuration if there's any error
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration.
        
        Returns:
            Default configuration
        """
        return {
            "default": {
                "provider": "litellm",
                "model": "gpt-3.5-turbo",
                "parameters": {
                    "temperature": 0.7,
                    "max_tokens": 500
                }
            }
        }
    
    def get_model_config(self, advisor_type: str) -> Dict[str, Any]:
        """Get model configuration for a specific advisor type.
        
        Args:
            advisor_type: Type of advisor (e.g., "savings", "risk", "investment")
            
        Returns:
            Model configuration for the specified advisor type
        """
        if advisor_type in self.config:
            return self.config[advisor_type]
        return self.config.get("default", self._get_default_config())
    
    def get_provider_name(self, advisor_type: str) -> str:
        """Get the provider name for a specific advisor type.
        
        Args:
            advisor_type: Type of advisor
            
        Returns:
            Provider name
        """
        config = self.get_model_config(advisor_type)
        return config.get("provider", "litellm")
    
    def get_model_name(self, advisor_type: str) -> str:
        """Get the model name for a specific advisor type.
        
        Args:
            advisor_type: Type of advisor
            
        Returns:
            Model name
        """
        config = self.get_model_config(advisor_type)
        return config.get("model", "gpt-3.5-turbo")


def main():
    """Main function for testing the config manager."""
    config_manager = LLMConfigManager()
    
    # Test getting configuration for different advisor types
    advisor_types = ["savings", "risk", "investment", "default"]
    
    for advisor_type in advisor_types:
        config = config_manager.get_model_config(advisor_type)
        print(f"Configuration for {advisor_type}: {config}")


if __name__ == "__main__":
    main()