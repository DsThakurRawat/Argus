# Copyright 2026 Divyansh Rawat
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Provider factory for managing LLM provider lifecycle.

This module provides the LLMProviderFactory, which handles the registration,
instantiation, and cleanup of various LLM providers based on configuration.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from .base import LLMProvider
from .config import LLMConfig, LLMProviderConfig
from .providers import (
    GeminiProvider,
    GrokProvider,
    GroqProvider,
    LiteLLMProvider,
    OllamaProvider,
    OpenAIProvider,
)

logger = logging.getLogger(__name__)

class LLMProviderFactory:
    """
    Registry and factory for LLM provider implementations.
    
    This class maintains a registry of supported providers and manages
    cached instances to ensure efficient resource reuse. Supports both
    class-level logic and instance-level logic for backward compatibility.
    """
    
    _providers_registry = {
        "gemini": GeminiProvider,
        "openai": OpenAIProvider,
        "ollama": OllamaProvider,
        "anthropic": LiteLLMProvider,
        "claude": LiteLLMProvider,
        "grok": GrokProvider,  # xAI Grok
        "groq": GroqProvider,  # Groq Inference
        "bedrock": LiteLLMProvider,
        "azure": LiteLLMProvider,
        "mistral": LiteLLMProvider,
        "perplexity": LiteLLMProvider,
        "openrouter": LiteLLMProvider,
        "xai": GrokProvider,
        "test_provider": LiteLLMProvider,
        "test": LiteLLMProvider,
    }
    _instances: dict[str, LLMProvider] = {}

    def __init__(self):
        """Initialize instance-level factory."""
        self._providers = {}
        self._provider_types = self._providers_registry.copy()

    def register_provider_type(self, provider_type: str, provider_class: type):
        """Register a new provider type."""
        self._provider_types[provider_type] = provider_class
        self.__class__._providers_registry[provider_type] = provider_class

    def create_provider(self, config: LLMProviderConfig, force_recreate: bool = False) -> LLMProvider:
        """Create a provider instance."""
        provider_type = config.provider
        if provider_type not in self._provider_types:
            raise ValueError(f"Unsupported provider type: {provider_type}")
        
        if not force_recreate and provider_type in self._providers:
            return self._providers[provider_type]
            
        provider_class = self._provider_types[provider_type]
        try:
            provider = provider_class(config)
            validate_func = getattr(provider, "validate_config", None)
            if callable(validate_func):
                try:
                    is_valid = validate_func()
                except TypeError:
                    is_valid = validate_func(config)
                if is_valid is False:
                    raise ValueError(f"Invalid configuration for provider: {provider_type}")
            self._providers[provider_type] = provider
            self.__class__._instances[f"{provider_type}_{getattr(config, 'model', 'default')}"] = provider
            return provider
        except ValueError:
            raise
        except Exception as e:
            raise RuntimeError(f"Provider creation failed: {e}")

    def get_provider(self, name: Union[str, LLMProviderConfig]) -> Any:
        """Hybrid get_provider: supports both string name and config object."""
        if isinstance(name, str):
            return self._providers.get(name)
        else:
            return self.get_provider_class(name)

    def get_all_providers(self) -> dict:
        """Get all registered providers."""
        return self._providers.copy()

    def remove_provider(self, name: str) -> bool:
        """Remove a registered provider."""
        if name in self._providers:
            del self._providers[name]
            return True
        return False

    def clear_providers(self) -> None:
        """Clear all registered providers."""
        self._providers.clear()

    def get_supported_providers(self) -> list:
        """Get all supported provider types."""
        return list(self._provider_types.keys())

    @classmethod
    def get_provider_class(cls, config: LLMProviderConfig) -> LLMProvider:
        """
        Get or create a provider instance from configuration (class method).
        """
        provider_type = config.provider
        if provider_type not in cls._providers_registry:
            raise ValueError(f"Unsupported provider type: {provider_type}")

        instance_key = f"{provider_type}_{getattr(config, 'model', 'default')}"
        if instance_key not in cls._instances:
            provider_class = cls._providers_registry[provider_type]
            cls._instances[instance_key] = provider_class(config)
        return cls._instances[instance_key]

    @classmethod
    def create_providers_from_config(cls, config: LLMConfig) -> dict[str, LLMProvider]:
        """
        Instantiate all providers defined in the global configuration.
        """
        providers = {}
        for provider_name, provider_config in config.providers.items():
            try:
                providers[provider_name] = cls.get_provider_class(provider_config)
            except Exception as e:
                logger.error(f"Failed to create provider '{provider_name}': {e}")
        return providers

    @classmethod
    async def shutdown(cls) -> None:
        """
        Gracefully shut down all registered provider instances.
        """
        for name, instance in list(cls._instances.items()):
            try:
                if hasattr(instance, "client") and hasattr(instance.client, "aclose"):
                    await instance.client.aclose()
                elif hasattr(instance, "__aexit__"):
                    await instance.__aexit__(None, None, None)
                logger.info(f"Successfully shut down provider: {name}")
            except Exception as e:
                logger.error(f"Error shutting down provider {name}: {e}")
        cls._instances.clear()

def get_provider_factory() -> type[LLMProviderFactory]:
    """Get the LLM provider factory class."""
    return LLMProviderFactory
