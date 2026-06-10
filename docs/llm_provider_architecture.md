# LLM Provider Abstraction Layer

## Architecture Overview

The LLM provider abstraction layer allows each advisor agent to use a different model while maintaining loose coupling and configuration-driven model selection. This design ensures that no advisor directly depends on a specific provider SDK.

## Folder Structure

```
llm_provider/
├── __init__.py
├── interface.py
├── config.py
├── factory.py
├── providers/
│   ├── __init__.py
│   ├── litellm_provider.py
│   └── mock_provider.py
```

## Interfaces

### LLMInterface (Abstract Base Class)
```python
class LLMInterface(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        pass
```

### LLMProvider (Abstract Base Class)
```python
class LLMProvider(ABC):
    @abstractmethod
    def get_provider_name(self) -> str:
        """Get the name of the provider."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available."""
        pass
    
    @abstractmethod
    def load_model(self, model_config: Dict[str, Any]) -> LLMInterface:
        """Load a model with the specified configuration."""
        pass
```

## Configuration Management

The configuration is managed through `llm_config.json` which defines the model to use for each advisor type:

```json
{
  "savings": {
    "provider": "litellm",
    "model": "gpt-4",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 500
    }
  },
  "risk": {
    "provider": "litellm",
    "model": "gpt-3.5-turbo",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 300
    }
  },
  "investment": {
    "provider": "litellm",
    "model": "claude-2",
    "parameters": {
      "temperature": 0.8,
      "max_tokens": 400
    }
  },
  "default": {
    "provider": "litellm",
    "model": "gpt-3.5-turbo",
    "parameters": {
      "temperature": 0.7,
      "max_tokens": 500
    }
  }
}
```

## Provider Adapters

### LiteLLM Provider
The LiteLLM provider supports multiple model backends through the LiteLLM library.

### Mock Provider
A mock provider for testing and development purposes.

## Model Selection Mechanism

The model selection mechanism works through the `LLMProviderFactory` which:
1. Reads the configuration for a specific advisor type
2. Selects the appropriate provider based on configuration
3. Creates an instance of the LLM interface for that provider
4. Returns the interface for use by the advisor

## Usage Example

```python
# Initialize configuration manager
config_manager = LLMConfigManager("llm_config.json")

# Initialize provider factory
factory = LLMProviderFactory()

# Get configuration for savings advisor
config = config_manager.get_model_config("savings")

# Create LLM instance for savings advisor
llm_instance = factory.create_llm_instance("savings", config_manager)

# Use the LLM instance
response = llm_instance.generate_response("Your prompt here")
```

## Benefits

1. **Provider Independence**: Advisors don't directly depend on provider SDKs
2. **Configuration-Driven**: Model selection is managed through configuration files
3. **Extensibility**: New providers can be easily added by implementing the LLMProvider interface
4. **Flexibility**: Each advisor can use a different model based on requirements
5. **Resilience**: Falls back to default configuration if a provider is unavailable