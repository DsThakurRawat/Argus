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

# argus/llm/monitoring/__init__.py

"""
LLM Monitoring and Observability Module.

This module provides comprehensive monitoring capabilities for LLM operations,
including structured logging, metrics collection, health checks, and dashboard APIs.
"""

from .dashboard_apis import LLMDashboardAPI
from .health_checks import CircuitBreakerHealthChecker, HealthStatus, LLMHealthChecker
from .llm_metrics import LLMMetricsCollector, LLMMetricType, get_llm_metrics_collector
from .structured_logging import (
    ErrorLogger,
    LLMRequestLogger,
    PerformanceLogger,
    StructuredLogger,
    clear_request_context,
    error_logger,
    get_request_context,
    performance_logger,
    request_logger,
    set_request_context,
)

__all__ = [
    # Health checks
    "HealthStatus",
    "LLMHealthChecker",
    "CircuitBreakerHealthChecker",
    # Metrics
    "LLMMetricType",
    "LLMMetricsCollector",
    "get_llm_metrics_collector",
    # Structured logging
    "StructuredLogger",
    "LLMRequestLogger",
    "PerformanceLogger",
    "ErrorLogger",
    "set_request_context",
    "clear_request_context",
    "get_request_context",
    "request_logger",
    "performance_logger",
    "error_logger",
    # Dashboard APIs
    "LLMDashboardAPI",
]
