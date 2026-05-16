# gemini_sre_agent/llm/providers/groq_provider.py

"""
Groq provider implementation.
Uses the OpenAI-compatible Groq API for ultra-fast inference.
"""

import logging
from typing import Any

from openai import AsyncOpenAI

from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)


class GroqProvider(LLMProvider):
    """Groq provider implementation."""

    def __init__(self, config: LLMProviderConfig) -> None:
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = config.base_url or "https://api.groq.com/openai/v1"

        # Initialize OpenAI client pointed at Groq
        self.client = AsyncOpenAI(
            api_key=self.api_key,
            base_url=str(self.base_url),
        )

    async def _generate(self, request: LLMRequest) -> LLMResponse:
        """Generate non-streaming response using Groq API."""
        logger.info(f"Generating response with Groq model: {self.model}")

        try:
            messages = self._convert_messages_to_openai_format(request.messages or [])
            
            # Groq specific defaults
            temperature = self.config.provider_specific.get("temperature", 0.7)
            max_tokens = self.config.provider_specific.get("max_tokens", 1024)

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            usage = {
                "input_tokens": response.usage.prompt_tokens if response.usage else 0,
                "output_tokens": response.usage.completion_tokens if response.usage else 0,
            }

            return LLMResponse(
                content=response.choices[0].message.content or "",
                model=self.model,
                provider="groq",
                usage=usage,
            )

        except Exception as e:
            logger.error(f"Groq generation error: {e}")
            raise

    def _convert_messages_to_openai_format(self, messages: list[dict[str, str]]) -> list[dict[str, str]]:
        return [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]

    async def health_check(self) -> bool:
        try:
            await self.client.models.list()
            return True
        except Exception:
            return False

    def get_available_models(self) -> dict[ModelType, str]:
        return {
            ModelType.FAST: "llama3-8b-8192",
            ModelType.SMART: "llama3-70b-8192",
            ModelType.CODE: "llama3-70b-8192",
        }
