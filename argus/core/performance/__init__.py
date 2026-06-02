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

"""Performance monitoring system for the Gemini SRE Agent.

This module provides comprehensive performance tracking and optimization including:
- Core performance metrics collection
- Asyncio profiling and async operation monitoring
- Performance alerting and threshold management
- Performance dashboards and visualization
- Performance optimization recommendations

The main components are:
- MetricsCollector: Core metrics collection and aggregation
- PerformanceProfiler: Asyncio and async operation profiling
- PerformanceAlerts: Alerting and threshold management
- PerformanceDashboard: Visualization and reporting
- OptimizationEngine: Performance optimization recommendations

Example usage:
    from argus.core.performance import MetricsCollector, PerformanceProfiler

    # Create metrics collector
    collector = MetricsCollector()
    
    # Track performance
    with collector.track_operation("api_call"):
        result = await api_call()
    
    # Profile async operations
    profiler = PerformanceProfiler()
    with profiler.profile_async_operation("data_processing"):
        await process_data()
"""

from .alerts import AlertConfig, AlertRule, AlertSeverity, AlertThreshold, PerformanceAlerts
from .dashboard import (
    DashboardConfig,
    DashboardWidget,
    PerformanceDashboard,
    PerformanceVisualization,
)
from .metrics import (
    MetricAggregation,
    MetricsCollector,
    MetricsConfig,
    MetricType,
    MetricValue,
    PerformanceMetrics,
)
from .optimization import (
    OptimizationConfig,
    OptimizationEngine,
    OptimizationRecommendation,
    PerformanceAnalyzer,
)
from .profiler import (
    AsyncProfiler,
    OperationProfile,
    PerformanceProfiler,
    ProfilerConfig,
    ProfilerResult,
)

__all__ = [
    # Metrics
    "MetricsCollector",
    "MetricType",
    "MetricValue",
    "MetricAggregation",
    "PerformanceMetrics",
    "MetricsConfig",

    # Profiler
    "PerformanceProfiler",
    "AsyncProfiler",
    "ProfilerConfig",
    "ProfilerResult",
    "OperationProfile",

    # Alerts
    "PerformanceAlerts",
    "AlertThreshold",
    "AlertRule",
    "AlertSeverity",
    "AlertConfig",

    # Dashboard
    "PerformanceDashboard",
    "DashboardConfig",
    "DashboardWidget",
    "PerformanceVisualization",

    # Optimization
    "OptimizationEngine",
    "OptimizationRecommendation",
    "PerformanceAnalyzer",
    "OptimizationConfig",
]
