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

# argus/ml/workflow/__init__.py

"""
Workflow package for the unified workflow orchestrator.

This package contains all workflow-related components including
context management, analysis, generation, validation, and metrics.
"""

from .workflow_analysis import AnalysisResult, WorkflowAnalysisEngine
from .workflow_context import WorkflowContextManager
from .workflow_generation import GenerationResult, WorkflowGenerationEngine
from .workflow_metrics import MetricData, WorkflowMetrics, WorkflowMetricsCollector
from .workflow_validation import ValidationResult, WorkflowValidationEngine

__all__ = [
    "AnalysisResult",
    "GenerationResult",
    "MetricData",
    "ValidationResult",
    "WorkflowAnalysisEngine",
    "WorkflowContextManager",
    "WorkflowGenerationEngine",
    "WorkflowMetrics",
    "WorkflowMetricsCollector",
    "WorkflowValidationEngine",
]
