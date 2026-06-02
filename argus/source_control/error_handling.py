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

# argus/source_control/error_handling.py

"""
Backward-compatible module for error handling components.

This module ensures that existing imports continue to work after the refactoring
into a subpackage.
"""

from .error_handling import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerOpenError,
    CircuitBreakerTimeoutError,
    CircuitState,
    ErrorClassification,
    ErrorClassifier,
    ErrorType,
    OperationCircuitBreakerConfig,
    ResilientOperationManager,
    RetryConfig,
    RetryManager,
    resilient_manager,
)

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerError",
    "CircuitBreakerOpenError",
    "CircuitBreakerTimeoutError",
    "CircuitState",
    "ErrorClassification",
    "ErrorClassifier",
    "ErrorType",
    "OperationCircuitBreakerConfig",
    "ResilientOperationManager",
    "RetryConfig",
    "RetryManager",
    "resilient_manager",
]
