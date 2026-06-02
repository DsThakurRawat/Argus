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

# argus/ingestion/monitoring/__init__.py

"""
Monitoring and observability components for the log ingestion system.

This module provides comprehensive monitoring capabilities including:
- Metrics collection and reporting
- Health checks and status monitoring
- Performance monitoring
- Alerting and notification systems
"""

from .alerts import Alert, AlertLevel, AlertManager
from .health import HealthChecker, HealthCheckResult, HealthStatus
from .metrics import MetricsCollector, MetricType, MetricValue
from .performance import PerformanceMetrics, PerformanceMonitor

__all__ = [
    "Alert",
    "AlertLevel",
    "AlertManager",
    "HealthCheckResult",
    "HealthChecker",
    "HealthStatus",
    "MetricType",
    "MetricValue",
    "MetricsCollector",
    "PerformanceMetrics",
    "PerformanceMonitor",
]
