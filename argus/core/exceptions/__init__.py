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
    "AgentConfigurationError",
    "AgentCoordinationError",
    "AgentError",
    "AgentExecutionError",
    # Agent-specific exceptions
    "AgentSpecificError",
    "AgentStateError",
    "AnalysisAgentError",
    # Base exceptions
    "ArgusAgentError",
    "ConfigurationError",
    "LLMAuthenticationError",
    "LLMConfigurationError",
    "LLMError",
    "LLMModelError",
    # LLM-specific exceptions
    "LLMProviderError",
    "LLMQuotaExceededError",
    "LLMRateLimitError",
    "LLMResponseError",
    "LLMTimeoutError",
    "MonitoringError",
    "ProcessingError",
    "PromptError",
    "RemediationAgentError",
    "ResilienceError",
    "ResponseError",
    "ServiceError",
    "TriageAgentError",
    "ValidationError",
]
