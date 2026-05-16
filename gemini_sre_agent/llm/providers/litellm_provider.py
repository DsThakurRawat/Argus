# gemini_sre_agent/llm/providers/litellm_provider.py

"""
Universal LiteLLM provider implementation.
Supports 100+ LLM providers using the LiteLLM library.
"""

import logging
from typing import Any, AsyncGenerator
import litellm

from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..capabilities.models import ModelCapability
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)

class LiteLLMProvider(LLMProvider):
    """Universal LiteLLM provider implementation."""

    def __init__(self, config: LLMProviderConfig) -> None:
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = str(config.base_url) if config.base_url else None

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """Generate response using litellm."""
        logger.info(f"Generating response with LiteLLM: {self.config.provider}/{self.model}")

        try:
            model_full_name = f"{self.config.provider}/{self.model}"
            if self.config.provider == "openai":
                model_full_name = self.model

            messages = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in (request.messages or [])]
            if request.prompt:
                messages.append({"role": "user", "content": request.prompt})

            # Respect request parameters with explicit None check
            temperature = request.temperature if request.temperature is not None else self.config.provider_specific.get("temperature", 0.7)
            max_tokens = request.max_tokens or self.config.provider_specific.get("max_tokens", 1024)

            response = await litellm.acompletion(
                model=model_full_name,
                messages=messages,
                api_key=self.api_key,
                api_base=self.base_url,
                temperature=temperature,
                max_tokens=max_tokens,
                tools=request.tools,
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
                tool_calls=getattr(response.choices[0].message, "tool_calls", None),
            )

        except Exception as e:
            logger.error(f"LiteLLM generation error: {e}")
            raise

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[LLMResponse, None]:
        """Generate streaming response using litellm."""
        model_full_name = f"{self.config.provider}/{self.model}"
        if self.config.provider == "openai":
            model_full_name = self.model
            
        messages = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in (request.messages or [])]
        if request.prompt:
            messages.append({"role": "user", "content": request.prompt})

        temperature = request.temperature if request.temperature is not None else self.config.provider_specific.get("temperature", 0.7)
        max_tokens = request.max_tokens or self.config.provider_specific.get("max_tokens", 1024)

        response = await litellm.acompletion(
            model=model_full_name,
            messages=messages,
            api_key=self.api_key,
            api_base=self.base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True
        )

        async for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                yield LLMResponse(
                    content=content,
                    model=self.model,
                    provider=self.config.provider,
                )

    async def health_check(self) -> bool:
        return True

    def supports_streaming(self) -> bool:
        return True

    def supports_tools(self) -> bool:
        return True

    def get_available_models(self) -> dict[ModelType, str]:
        # Return intelligent defaults based on the provider
        if self.config.provider == "azure":
            return {ModelType.FAST: "gpt-35-turbo", ModelType.SMART: "gpt-4o"}
        if self.config.provider == "mistral":
            return {ModelType.FAST: "mistral-small-latest", ModelType.SMART: "mistral-large-latest"}
        
        return {
            ModelType.FAST: self.model,
            ModelType.SMART: self.model,
        }

    async def embeddings(self, text: str) -> list[float]:
        response = await litellm.aembedding(
            model=f"{self.config.provider}/{self.model}",
            input=[text],
            api_key=self.api_key,
            api_base=self.base_url
        )
        return response.data[0].embedding

    def token_count(self, text: str) -> int:
        return litellm.token_counter(model=self.model, text=text)

    def cost_estimate(self, input_tokens: int, output_tokens: int) -> float:
        try:
            return litellm.completion_cost(model=self.model, prompt_tokens=input_tokens, completion_tokens=output_tokens)
        except Exception:
            return 0.0

    @classmethod
    def validate_config(cls, config: Any) -> None:
        if not hasattr(config, "api_key") or not config.api_key:
            if config.provider != "ollama":
                raise ValueError(f"API key is required for provider {config.provider}")

    def get_custom_capabilities(self) -> list[ModelCapability]:
        return []
