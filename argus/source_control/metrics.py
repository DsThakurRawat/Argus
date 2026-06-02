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

# argus/source_control/metrics.py

"""
Backward-compatible module for metrics.

This module ensures that existing imports of metrics classes continue to work
after the refactoring into a subpackage.
"""

from .metrics.analyzers import MetricsAnalyzer
from .metrics.collectors import MetricsCollector, OperationMetrics
from .metrics.core import MetricPoint, MetricSeries, MetricType

__all__ = [
    "MetricPoint",
    "MetricSeries",
    "MetricType",
    "MetricsAnalyzer",
    "MetricsCollector",
    "OperationMetrics",
]
