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

# gemini_sre_agent/llm/__init__.py

"""
Multi-LLM Provider Support System

This module provides a unified interface for multiple LLM providers including
Gemini, Ollama, Claude, ChatGPT, Grok, and Amazon Bedrock with advanced
model mixing capabilities, cost optimization, and enterprise-grade resilience.
"""

from .base import (
    CircuitBreaker,
    ErrorSeverity,
    LLMProvider,
    LLMProviderError,
    LLMRequest,
    LLMResponse,
)
from .common.enums import ModelType, ProviderType
from .factory import LLMProviderFactory
from .providers import (
    AnthropicProvider,
    BedrockProvider,
    GeminiProvider,
    GrokProvider,
    OllamaProvider,
    OpenAIProvider,
)

__all__ = [
    "LLMProvider",
    "LLMRequest",
    "LLMResponse",
    "ModelType",
    "ProviderType",
    "ErrorSeverity",
    "LLMProviderError",
    "CircuitBreaker",
    "LLMProviderFactory",
    # Concrete providers
    "GeminiProvider",
    "OpenAIProvider",
    "AnthropicProvider",
    "OllamaProvider",
    "GrokProvider",
    "BedrockProvider",
]
