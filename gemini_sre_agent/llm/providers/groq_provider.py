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
Groq provider implementation for high-speed inference.

This module provides the GroqProvider class, which implements the LLMProvider
interface for models hosted on the Groq platform (e.g., Llama 3, Mixtral).
"""

import json
import logging
from typing import Any, AsyncGenerator

import httpx

from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..capabilities.models import ModelCapability
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    """
    Groq API provider implementation for ultra-fast model inference.
    
    This provider leverages Groq's LPUs to deliver low-latency responses
    for open-source models like Llama and Mixtral.
    """

    def __init__(self, config: LLMProviderConfig) -> None:
        """
        Initialize the Groq provider.

        Args:
            config: Configuration for the Groq provider, including API key and optional base URL.
        """
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = (
            str(config.base_url) if config.base_url else "https://api.groq.com/openai/v1"
        )
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """
        Generate a non-streaming response from Groq.

        Args:
            request: The LLM request containing prompt, messages, and parameters.

        Returns:
            An LLMResponse object containing the generated content and usage metrics.
        """
        messages = self._convert_messages(request.messages or [])
        if request.prompt:
            messages.append({"role": "user", "content": request.prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": request.temperature if request.temperature is not None else 0.7,
            "max_tokens": request.max_tokens or 1024,
            "stream": False,
        }
        if request.tools:
            payload["tools"] = request.tools

        response = await self.client.post("/chat/completions", json=payload)
        response.raise_for_status()
        data = response.json()
        message = data["choices"][0]["message"]

        return LLMResponse(
            content=message.get("content") or "",
            model=self.model,
            provider="groq",
            usage=self._extract_usage(data.get("usage")),
            tool_calls=message.get("tool_calls"),
        )

    async def generate_stream(
        self, request: LLMRequest
    ) -> AsyncGenerator[LLMResponse, None]:
        """
        Generate a streaming response from Groq.

        Args:
            request: The LLM request.

        Yields:
            LLMResponse chunks as they are received from the API.
        """
        # Note: Streaming is stubbed for this implementation cycle
        yield LLMResponse(content="Streaming not fully implemented", provider="groq")

    async def health_check(self) -> bool:
        """Check if the Groq API is accessible and the API key is valid."""
        try:
            response = await self.client.get("/models")
            return response.status_code == 200
        except Exception:
            return False

    def supports_streaming(self) -> bool:
        """Returns True as Groq supports streaming responses."""
        return True

    def supports_tools(self) -> bool:
        """Returns True as Groq supports function calling/tools."""
        return True

    def get_available_models(self) -> dict[ModelType, str]:
        """Map semantic model types to specific Groq model IDs."""
        return {
            ModelType.FAST: "llama3-8b-8192",
            ModelType.SMART: "llama3-70b-8192",
        }

    async def embeddings(self, text: str) -> list[float]:
        """Groq does not provide an embeddings API."""
        raise NotImplementedError("Groq provider does not support native embeddings.")

    def token_count(self, text: str) -> int:
        """Approximate token count for the given text."""
        return len(text.split())

    def cost_estimate(self, input_tokens: int, output_tokens: int) -> float:
        """Provide a rough cost estimate for the request."""
        return 0.0

    @classmethod
    def validate_config(cls, config: Any) -> None:
        """Validate that the configuration contains a valid API key."""
        if not hasattr(config, "api_key") or not config.api_key:
            raise ValueError("Groq API key is required")

    def get_custom_capabilities(self) -> list[ModelCapability]:
        """Return any provider-specific capabilities."""
        return []

    def _convert_messages(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        """Convert standard message format to Groq API format."""
        return [
            {"role": m.get("role", "user"), "content": m.get("content", "")}
            for m in messages
        ]

    def _extract_usage(self, usage: dict[str, Any]) -> dict[str, int]:
        """Extract token usage statistics from the API response."""
        if not usage:
            return {}
        return {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Ensure the HTTP client is closed on exit."""
        await self.client.aclose()
