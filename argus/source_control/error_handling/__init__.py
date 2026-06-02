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

# argus/source_control/error_handling/__init__.py

"""
Error handling and resilience patterns package.

This package provides comprehensive error handling, circuit breaker patterns,
retry mechanisms, and error classification for robust source control operations.
"""

from .circuit_breaker import CircuitBreaker
from .core import (
    CircuitBreakerConfig,
    CircuitBreakerError,
    CircuitBreakerOpenError,
    CircuitBreakerTimeoutError,
    CircuitState,
    ErrorClassification,
    ErrorType,
    OperationCircuitBreakerConfig,
    RetryConfig,
)
from .error_classification import ErrorClassifier
from .factory import (
    ErrorHandlingFactory,
    create_error_handling_factory,
    create_provider_error_handling,
    create_provider_error_handling_with_preset,
    get_provider_config,
)
from .graceful_degradation import (
    GracefulDegradationManager,
    create_graceful_degradation_manager,
)
from .health_checks import HealthCheckManager, create_health_check_endpoints
from .metrics_integration import ErrorHandlingMetrics
from .resilient_operations import ResilientOperationManager, resilient_manager
from .retry_manager import RetryManager

__all__ = [
    "CircuitBreaker",
    "CircuitBreakerConfig",
    "CircuitBreakerError",
    "CircuitBreakerOpenError",
    "CircuitBreakerTimeoutError",
    "CircuitState",
    "ErrorClassification",
    "ErrorClassifier",
    "ErrorHandlingFactory",
    "ErrorHandlingMetrics",
    "ErrorType",
    "GracefulDegradationManager",
    "HealthCheckManager",
    "OperationCircuitBreakerConfig",
    "ResilientOperationManager",
    "RetryConfig",
    "RetryManager",
    "create_error_handling_factory",
    "create_graceful_degradation_manager",
    "create_health_check_endpoints",
    "create_provider_error_handling",
    "create_provider_error_handling_with_preset",
    "get_provider_config",
    "resilient_manager",
]
