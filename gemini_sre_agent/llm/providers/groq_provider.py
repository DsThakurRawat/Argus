# gemini_sre_agent/llm/providers/groq_provider.py

"""
Groq provider implementation.

This module contains the concrete implementation of the LLMProvider interface
for various open-source models (via Groq API).
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
    """Groq API provider implementation."""

    def __init__(self, config: LLMProviderConfig) -> None:
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = (
            str(config.base_url) if config.base_url else "https://api.groq.com/openai/v1"
        )

        # Initialize HTTP client
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """Generate non-streaming response using Groq API."""
        logger.info(f"Generating response with Groq model: {self.model}")

        try:
            # Convert messages to format and include prompt if present
            messages = self._convert_messages_to_groq_format(request.messages or [])
            if request.prompt:
                messages.append({"role": "user", "content": request.prompt})

            # Respect request parameters with explicit None check for deterministic 0.0
            temperature = request.temperature if request.temperature is not None else self.config.provider_specific.get("temperature", 0.7)
            max_tokens = request.max_tokens or self.config.provider_specific.get("max_tokens", 1024)
            top_p = self.config.provider_specific.get("top_p", 1.0)

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "stream": False,
            }
            
            # Pass tools if available
            if request.tools:
                payload["tools"] = request.tools

            response = await self.client.post("/chat/completions", json=payload)
            response.raise_for_status()

            data = response.json()
            message = data["choices"][0]["message"]
            usage = self._extract_usage(data.get("usage"))

            return LLMResponse(
                content=message.get("content") or "",
                model=self.model,
                provider=self.provider_name,
                usage=usage,
                tool_calls=message.get("tool_calls"),
            )

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[LLMResponse, None]:
        """Generate streaming response using Groq API."""
        logger.info(f"Generating streaming response with Groq model: {self.model}")

        try:
            messages = self._convert_messages_to_groq_format(request.messages or [])
            if request.prompt:
                messages.append({"role": "user", "content": request.prompt})

            temperature = request.temperature if request.temperature is not None else self.config.provider_specific.get("temperature", 0.7)
            max_tokens = request.max_tokens or self.config.provider_specific.get("max_tokens", 1024)

            payload = {
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True,
            }

            async with self.client.stream("POST", "/chat/completions", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        if data_str.strip() == "[DONE]":
                            break
                        try:
                            data = json.loads(data_str)
                            if data.get("choices"):
                                delta = data["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield LLMResponse(
                                        content=delta["content"],
                                        model=self.model,
                                        provider=self.provider_name,
                                    )
                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            logger.error(f"Groq streaming error: {e}")
            raise

    async def health_check(self) -> bool:
        """Check if Groq API is accessible."""
        try:
            response = await self.client.get("/models")
            return response.status_code == 200
        except Exception:
            return False

    def supports_streaming(self) -> bool:
        return True

    def supports_tools(self) -> bool:
        return True

    def get_available_models(self) -> dict[ModelType, str]:
        return {
            ModelType.FAST: "llama3-8b-8192",
            ModelType.SMART: "llama3-70b-8192",
            ModelType.CODE: "llama3-70b-8192",
            ModelType.ANALYSIS: "llama3-70b-8192",
        }

    async def embeddings(self, text: str) -> list[float]:
        """Groq does not support native embeddings."""
        raise NotImplementedError("Groq provider does not support native embeddings yet.")

    def token_count(self, text: str) -> int:
        return len(text.split()) * 1.3

    def cost_estimate(self, input_tokens: int, output_tokens: int) -> float:
        return (input_tokens * 0.0000005) + (output_tokens * 0.0000008)

    @classmethod
    def validate_config(cls, config: Any) -> None:
        if not hasattr(config, "api_key") or not config.api_key:
            raise ValueError("Groq API key is required")

    def get_custom_capabilities(self) -> list[ModelCapability]:
        return []

    def _convert_messages_to_groq_format(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        return [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]

    def _extract_usage(self, usage: Any) -> dict[str, int]:
        if not usage:
            return {"input_tokens": 0, "output_tokens": 0}
        return {
            "input_tokens": usage.get("prompt_tokens", 0),
            "output_tokens": usage.get("completion_tokens", 0),
        }

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()
