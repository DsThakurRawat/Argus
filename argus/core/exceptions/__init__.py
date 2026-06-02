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

# argus/core/exceptions/__init__.py

"""
Core exception classes for the Gemini SRE Agent system.

This package provides a comprehensive exception hierarchy for error handling
across all components of the system.
"""

from .agent import (
    AgentConfigurationError,
    AgentCoordinationError,
    AgentExecutionError,
    AgentStateError,
    AnalysisAgentError,
    PromptError,
    RemediationAgentError,
    ResponseError,
    TriageAgentError,
)
from .agent import AgentError as AgentSpecificError
from .base import (
    AgentError,
    ConfigurationError,
    ArgusAgentError,
    LLMError,
    MonitoringError,
    ProcessingError,
    ResilienceError,
    ServiceError,
    ValidationError,
)
from .llm import (
    LLMAuthenticationError,
    LLMConfigurationError,
    LLMModelError,
    LLMProviderError,
    LLMQuotaExceededError,
    LLMRateLimitError,
    LLMResponseError,
    LLMTimeoutError,
)

__all__ = [
    # Base exceptions
    "ArgusAgentError",
    "ConfigurationError",
    "ValidationError",
    "ServiceError",
    "ProcessingError",
    "AgentError",
    "LLMError",
    "MonitoringError",
    "ResilienceError",
    # Agent-specific exceptions
    "AgentSpecificError",
    "PromptError",
    "ResponseError",
    "AgentExecutionError",
    "AgentConfigurationError",
    "AgentStateError",
    "AgentCoordinationError",
    "TriageAgentError",
    "AnalysisAgentError",
    "RemediationAgentError",
    # LLM-specific exceptions
    "LLMProviderError",
    "LLMModelError",
    "LLMResponseError",
    "LLMConfigurationError",
    "LLMRateLimitError",
    "LLMAuthenticationError",
    "LLMTimeoutError",
    "LLMQuotaExceededError",
]
