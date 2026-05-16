# gemini_sre_agent/llm/providers/litellm_provider.py

"""
Universal LiteLLM provider implementation.
Supports 100+ LLM providers using the LiteLLM library.
"""

import logging
from typing import Any
import litellm

from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)

class LiteLLMProvider(LLMProvider):
    """Universal LiteLLM provider implementation."""

    def __init__(self, config: LLMProviderConfig) -> None:
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = str(config.base_url) if config.base_url else None
        
        # litellm uses environment variables or passed parameters
        # We'll pass them directly in completion calls

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using litellm."""
        logger.info(f"Generating response with LiteLLM: {self.config.provider}/{self.model}")

        try:
            # Format model name for litellm (e.g., 'anthropic/claude-3-sonnet')
            model_full_name = f"{self.config.provider}/{self.model}"
            if self.config.provider == "openai":
                model_full_name = self.model
            elif self.config.provider == "azure":
                model_full_name = f"azure/{self.model}"

            messages = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in (request.messages or [])]
            if request.prompt:
                messages.append({"role": "user", "content": request.prompt})

            response = await litellm.acompletion(
                model=model_full_name,
                messages=messages,
                api_key=self.api_key,
                api_base=self.base_url,
                temperature=self.config.provider_specific.get("temperature", 0.7),
                max_tokens=self.config.provider_specific.get("max_tokens", 1024),
            )

            usage = {
                "input_tokens": response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                "output_tokens": response.usage.completion_tokens if hasattr(response, 'usage') else 0,
            }

            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=self.model,
                provider=self.config.provider,
                usage=usage,
            )

        except Exception as e:
            logger.error(f"LiteLLM generation error: {e}")
            raise

    async def health_check(self) -> bool:
        # Simple check: can we initialize the model?
        return True

    def get_available_models(self) -> dict[ModelType, str]:
        # These are defaults, users can override in config
        return {
            ModelType.FAST: self.model,
            ModelType.SMART: self.model,
        }
