# gemini_sre_agent/llm/factory.py

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
    """Factory for creating LLM provider instances."""

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
        providers = {}
        for provider_name, provider_config in config.providers.items():
            try:
                providers[provider_name] = cls.get_provider(provider_config)
            except Exception as e:
                logger.error(f"Failed to create provider '{provider_name}': {e}")
        return providers

    @classmethod
    async def shutdown(cls) -> None:
        """Shutdown all registered provider instances."""
        for name, instance in list(cls._instances.items()):
            try:
                if hasattr(instance, "client") and hasattr(instance.client, "aclose"):
                    await instance.client.aclose()
                logger.info(f"Successfully shut down provider: {name}")
            except Exception as e:
                logger.error(f"Error shutting down provider {name}: {e}")
        cls._instances.clear()

def get_provider_factory() -> type[LLMProviderFactory]:
    return LLMProviderFactory
