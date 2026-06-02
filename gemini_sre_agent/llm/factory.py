# Copyright 2026 divyanshrawat
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
from typing import Any

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
    cached instances to ensure efficient resource reuse.
    """

    _providers = {
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
    }
    _instances: dict[str, LLMProvider] = {}

    @classmethod
    def get_provider(cls, config: LLMProviderConfig) -> LLMProvider:
        """
        Get or create a provider instance from configuration.

        Args:
            config: The provider-specific configuration.

        Returns:
            An instantiated LLMProvider ready for requests.

        Raises:
            ValueError: If the provider type is not found in the registry.
        """
        provider_type = config.provider
        if provider_type not in cls._providers:
            raise ValueError(f"Unsupported provider type: {provider_type}")

        instance_key = f"{provider_type}_{getattr(config, 'model', 'default')}"
        if instance_key not in cls._instances:
            provider_class = cls._providers[provider_type]
            cls._instances[instance_key] = provider_class(config)
        return cls._instances[instance_key]

    @classmethod
    def create_providers_from_config(cls, config: LLMConfig) -> dict[str, LLMProvider]:
        """
        Instantiate all providers defined in the global configuration.

        Args:
            config: The root LLM configuration object.

        Returns:
            A dictionary mapping provider names to their instances.
        """
        providers = {}
        for provider_name, provider_config in config.providers.items():
            try:
                providers[provider_name] = cls.get_provider(provider_config)
            except Exception as e:
                logger.error(f"Failed to create provider '{provider_name}': {e}")
        return providers

    @classmethod
    async def shutdown(cls) -> None:
        """
        Gracefully shut down all registered provider instances.
        
        This method ensures that any underlying HTTP clients or persistent
        connections are closed correctly during application shutdown.
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
