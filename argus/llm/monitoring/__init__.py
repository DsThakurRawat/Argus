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
    "CircuitBreakerHealthChecker",
    "ErrorLogger",
    # Health checks
    "HealthStatus",
    # Dashboard APIs
    "LLMDashboardAPI",
    "LLMHealthChecker",
    # Metrics
    "LLMMetricType",
    "LLMMetricsCollector",
    "LLMRequestLogger",
    "PerformanceLogger",
    # Structured logging
    "StructuredLogger",
    "clear_request_context",
    "error_logger",
    "get_llm_metrics_collector",
    "get_request_context",
    "performance_logger",
    "request_logger",
    "set_request_context",
]
