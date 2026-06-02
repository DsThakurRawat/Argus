#

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
    ArgusAgentError,
    ConfigurationError,
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
