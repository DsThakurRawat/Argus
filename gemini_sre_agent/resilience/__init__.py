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

# gemini_sre_agent/resilience/__init__.py

"""Resilience patterns and error handling module for the Gemini SRE Agent."""

from .circuit_breaker import CircuitBreaker, CircuitState
from .error_classifier import ErrorCategory, ErrorClassifier
from .fallback_manager import FallbackManager
from .resilience_manager import ResilienceManager
from .retry_handler import RetryHandler

__all__ = [
    "CircuitBreaker",
    "CircuitState",
    "ErrorCategory",
    "ErrorClassifier",
    "FallbackManager",
    "ResilienceManager",
    "RetryHandler",
]
