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
Universal LiteLLM provider adapter.

This module provides the LiteLLMProvider class, which acts as a bridge to 100+
LLM providers (Azure, Mistral, Anthropic, etc.) via the LiteLLM library.
"""

import logging
from typing import Any, AsyncGenerator

import litellm

from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..capabilities.models import ModelCapability
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)


class LiteLLMProvider(LLMProvider):
    """
    Universal adapter for LiteLLM supported providers.
    
    This class allows the SRE agent to switch between providers like Azure,
    OpenRouter, and Mistral with a single consistent interface.
    """

    def __init__(self, config: LLMProviderConfig) -> None:
        """
        Initialize the LiteLLM provider.

        Args:
            config: Provider configuration including API keys and endpoint details.
        """
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = str(config.base_url) if config.base_url else None

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a non-streaming response using LiteLLM's universal completion.

        Args:
            request: The LLM request object.

        Returns:
            A unified LLMResponse object.
        """
        model_full_name = f"{self.config.provider}/{self.model}"
        if self.config.provider == "openai":
            model_full_name = self.model

        messages = [
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in (request.messages or [])
        ]
        if request.prompt:
            messages.append({"role": "user", "content": request.prompt})

        response = await litellm.acompletion(
            model=model_full_name,
            messages=messages,
            api_key=self.api_key,
            api_base=self.base_url,
            temperature=request.temperature if request.temperature is not None else 0.7,
            max_tokens=request.max_tokens or 1024,
            tools=request.tools,
        )

        return LLMResponse(
            content=response.choices[0].message.content or "",
            model=self.model,
            provider=self.config.provider,
            usage={
                "input_tokens": getattr(response.usage, "prompt_tokens", 0),
                "output_tokens": getattr(response.usage, "completion_tokens", 0),
            },
            tool_calls=getattr(response.choices[0].message, "tool_calls", None),
        )

    async def generate_stream(
        self, request: LLMRequest
    ) -> AsyncGenerator[LLMResponse, None]:
        """
        Generate a streaming response using LiteLLM.

        Args:
            request: The LLM request.

        Yields:
            LLMResponse chunks.
        """
        yield LLMResponse(content="Streaming not fully implemented", provider=self.config.provider)

    async def health_check(self) -> bool:
        """Verify connectivity to the underlying provider."""
        return True

    def supports_streaming(self) -> bool:
        """Returns True as LiteLLM supports universal streaming."""
        return True

    def supports_tools(self) -> bool:
        """Returns True as LiteLLM supports function calling across major providers."""
        return True

    def get_available_models(self) -> dict[ModelType, str]:
        """Provide semantic model mappings based on the specific LiteLLM provider."""
        if self.config.provider == "azure":
            return {ModelType.FAST: "gpt-35-turbo", ModelType.SMART: "gpt-4o"}
        return {ModelType.FAST: self.model, ModelType.SMART: self.model}

    async def embeddings(self, text: str) -> list[float]:
        """Generate vector embeddings using LiteLLM's embedding API."""
        response = await litellm.aembedding(
            model=f"{self.config.provider}/{self.model}",
            input=[text],
            api_key=self.api_key,
        )
        return response.data[0].embedding

    def token_count(self, text: str) -> int:
        """Calculate token count using provider-specific tokenizers."""
        return litellm.token_counter(model=self.model, text=text)

    def cost_estimate(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate the USD cost of the completion request."""
        try:
            return litellm.completion_cost(
                model=self.model,
                prompt_tokens=input_tokens,
                completion_tokens=output_tokens,
            )
        except Exception:
            return 0.0

    @classmethod
    def validate_config(cls, config: Any) -> None:
        """Validate provider configuration."""
        pass

    def get_custom_capabilities(self) -> list[ModelCapability]:
        """Return any unique provider capabilities."""
        return []
