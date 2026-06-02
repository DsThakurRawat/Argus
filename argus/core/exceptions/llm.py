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

# argus/core/exceptions/llm.py

"""
LLM-specific exception classes.

This module defines exceptions specific to LLM operations, including
provider errors, model errors, and response processing errors.
"""


from .base import LLMError


class LLMProviderError(LLMError):
    """
    Exception raised for LLM provider-related errors.

    This exception is raised when there are issues with LLM providers,
    such as authentication failures, rate limiting, or service unavailability.
    """

    pass


class LLMModelError(LLMError):
    """
    Exception raised for LLM model-related errors.

    This exception is raised when there are issues with specific models,
    such as model not found, unsupported features, or model-specific errors.
    """

    pass


class LLMResponseError(LLMError):
    """
    Exception raised for LLM response processing errors.

    This exception is raised when there are issues processing LLM responses,
    such as invalid response format, parsing errors, or content validation failures.
    """

    pass


class LLMConfigurationError(LLMError):
    """
    Exception raised for LLM configuration errors.

    This exception is raised when there are issues with LLM configuration,
    such as invalid model parameters, missing API keys, or configuration conflicts.
    """

    pass


class LLMRateLimitError(LLMProviderError):
    """
    Exception raised when LLM rate limits are exceeded.

    This exception is raised when the LLM provider rate limits are exceeded
    and requests are being throttled.
    """

    def __init__(
        self, message: str, retry_after: int | None = None, **kwargs
    ) -> None:
        """
        Initialize the rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
            **kwargs: Additional arguments for base exception
        """
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class LLMAuthenticationError(LLMProviderError):
    """
    Exception raised for LLM authentication errors.

    This exception is raised when there are authentication issues with
    LLM providers, such as invalid API keys or expired tokens.
    """

    pass


class LLMTimeoutError(LLMProviderError):
    """
    Exception raised for LLM timeout errors.

    This exception is raised when LLM requests timeout or take too long
    to complete.
    """

    pass


class LLMQuotaExceededError(LLMProviderError):
    """
    Exception raised when LLM quota is exceeded.

    This exception is raised when the LLM provider quota is exceeded
    and no more requests can be made.
    """

    pass
