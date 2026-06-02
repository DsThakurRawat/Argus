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

# gemini_sre_agent/ml/performance/__init__.py

"""
Performance optimization module.

This module provides performance optimizations for the enhanced code generation
system, including caching, async processing, and parallel analysis.
"""

from .async_optimizer import (
    AsyncOptimizer,
    AsyncTask,
    BatchResult,
    cleanup_async_optimizer,
    get_async_optimizer,
)
from .performance_config import (
    AnalysisConfig,
    CacheConfig,
    ModelPerformanceConfig,
    PerformanceConfig,
)
from .performance_monitor import (
    OperationRecorder,
    PerformanceMetric,
    PerformanceMonitor,
    PerformanceSummary,
    get_performance_monitor,
    get_performance_summary,
    record_performance,
)
from .repository_analyzer import PerformanceRepositoryAnalyzer

__all__ = [
    "AnalysisConfig",
    "AsyncOptimizer",
    "AsyncTask",
    "BatchResult",
    "CacheConfig",
    "ModelPerformanceConfig",
    "OperationRecorder",
    "PerformanceConfig",
    "PerformanceMetric",
    "PerformanceMonitor",
    "PerformanceRepositoryAnalyzer",
    "PerformanceSummary",
    "cleanup_async_optimizer",
    "get_async_optimizer",
    "get_performance_monitor",
    "get_performance_summary",
    "record_performance",
]
