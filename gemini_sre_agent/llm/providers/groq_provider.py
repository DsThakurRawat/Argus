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

# gemini_sre_agent/llm/providers/groq_provider.py

import json
import logging
from typing import Any, AsyncGenerator
import httpx
from ..base import LLMProvider, LLMRequest, LLMResponse, ModelType
from ..capabilities.models import ModelCapability
from ..config import LLMProviderConfig

logger = logging.getLogger(__name__)

class GroqProvider(LLMProvider):
    """Groq API provider implementation (Llama 3, etc. via Groq)."""

    def __init__(self, config: LLMProviderConfig) -> None:
        super().__init__(config)
        self.api_key = config.api_key
        self.base_url = str(config.base_url) if config.base_url else "https://api.groq.com/openai/v1"
        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            timeout=30.0,
        )

    async def _generate(self, request: LLMRequest) -> LLMResponse:
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

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[LLMResponse, None]:
        # Implementation for streaming...
        yield LLMResponse(content="Streaming not fully implemented in scratch", provider="groq")

    async def health_check(self) -> bool:
        return True

    def supports_streaming(self) -> bool: return True
    def supports_tools(self) -> bool: return True
    def get_available_models(self) -> dict[ModelType, str]:
        return {ModelType.FAST: "llama3-8b-8192", ModelType.SMART: "llama3-70b-8192"}
    
    async def embeddings(self, text: str) -> list[float]: raise NotImplementedError()
    def token_count(self, text: str) -> int: return len(text.split())
    def cost_estimate(self, i, o) -> float: return 0.0
    @classmethod
    def validate_config(cls, config: Any) -> None: pass
    def get_custom_capabilities(self) -> list[ModelCapability]: return []
    def _convert_messages(self, messages): return [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in messages]
    def _extract_usage(self, usage): return {"input_tokens": usage.get("prompt_tokens", 0), "output_tokens": usage.get("completion_tokens", 0)} if usage else {}

    async def __aenter__(self): return self
    async def __aexit__(self, et, ev, tb): await self.client.aclose()
