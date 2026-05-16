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

# gemini_sre_agent/llm/providers/litellm_provider.py

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
        model_full_name = f"{self.config.provider}/{self.model}"
        if self.config.provider == "openai":
            model_full_name = self.model

        messages = [{"role": m.get("role", "user"), "content": m.get("content", "")} for m in (request.messages or [])]
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
            usage={"input_tokens": getattr(response.usage, "prompt_tokens", 0), "output_tokens": getattr(response.usage, "completion_tokens", 0)},
            tool_calls=getattr(response.choices[0].message, "tool_calls", None),
        )

    async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[LLMResponse, None]:
        yield LLMResponse(content="Streaming not fully implemented in scratch", provider=self.config.provider)

    async def health_check(self) -> bool: return True
    def supports_streaming(self) -> bool: return True
    def supports_tools(self) -> bool: return True
    def get_available_models(self) -> dict[ModelType, str]:
        if self.config.provider == "azure":
            return {ModelType.FAST: "gpt-35-turbo", ModelType.SMART: "gpt-4o"}
        return {ModelType.FAST: self.model, ModelType.SMART: self.model}
    
    async def embeddings(self, text: str) -> list[float]:
        response = await litellm.aembedding(model=f"{self.config.provider}/{self.model}", input=[text], api_key=self.api_key)
        return response.data[0].embedding

    def token_count(self, text: str) -> int: return litellm.token_counter(model=self.model, text=text)
    def cost_estimate(self, i, o) -> float: return 0.0
    @classmethod
    def validate_config(cls, config: Any) -> None: pass
    def get_custom_capabilities(self) -> list[ModelCapability]: return []
