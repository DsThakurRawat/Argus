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

# gemini_sre_agent/core/exceptions/base.py

"""
Base exception hierarchy for the Gemini SRE Agent system.

This module defines the core exception classes that form the foundation
of the error handling system across all components.
"""

from typing import Any


class ArgusAgentError(Exception):
    """
    Base exception class for all Gemini SRE Agent errors.

    This is the root exception class that all other exceptions in the system
    should inherit from. It provides common functionality for error handling
    and logging.

    Attributes:
        message: The error message describing what went wrong
        error_code: Optional error code for programmatic error handling
        details: Optional dictionary containing additional error details
        original_error: Optional reference to the original exception that caused this error
    """

    def __init__(
        self,
        message: str,
        error_code: str | None = None,
        details: dict[str, Any] | None = None,
        original_error: Exception | None = None,
    ) -> None:
        """
        Initialize the base exception.

        Args:
            message: Human-readable error message
            error_code: Optional error code for programmatic handling
            details: Optional additional error details
            original_error: Optional original exception that caused this error
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        self.original_error = original_error

    def __str__(self) -> str:
        """Return string representation of the exception."""
        base_msg = f"{self.__class__.__name__}: {self.message}"
        if self.error_code:
            base_msg += f" (Code: {self.error_code})"
        return base_msg

    def to_dict(self) -> dict[str, Any]:
        """
        Convert exception to dictionary for serialization.

        Returns:
            Dictionary representation of the exception
        """
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "error_code": self.error_code,
            "details": self.details,
            "original_error": str(self.original_error) if self.original_error else None,
        }


class ConfigurationError(ArgusAgentError):
    """
    Exception raised for configuration-related errors.

    This exception is raised when there are issues with configuration
    files, environment variables, or configuration validation.
    """

    pass


class ValidationError(ArgusAgentError):
    """
    Exception raised for data validation errors.

    This exception is raised when input data fails validation checks
    or when data format is incorrect.
    """

    pass


class ServiceError(ArgusAgentError):
    """
    Exception raised for service-related errors.

    This exception is raised when there are issues with external services,
    API calls, or service availability.
    """

    pass


class ProcessingError(ArgusAgentError):
    """
    Exception raised for data processing errors.

    This exception is raised when there are issues during data processing,
    analysis, or transformation operations.
    """

    pass


class AgentError(ArgusAgentError):
    """
    Exception raised for agent-related errors.

    This exception is raised when there are issues with agent operations,
    such as prompt processing, response generation, or agent coordination.
    """

    pass


class LLMError(ArgusAgentError):
    """
    Exception raised for LLM-related errors.

    This exception is raised when there are issues with LLM providers,
    API calls, model responses, or LLM configuration.
    """

    pass


class MonitoringError(ArgusAgentError):
    """
    Exception raised for monitoring-related errors.

    This exception is raised when there are issues with monitoring systems,
    metrics collection, or alerting.
    """

    pass


class ResilienceError(ArgusAgentError):
    """
    Exception raised for resilience-related errors.

    This exception is raised when there are issues with circuit breakers,
    retry mechanisms, or other resilience patterns.
    """

    pass
