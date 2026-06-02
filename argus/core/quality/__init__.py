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

# argus/core/quality/__init__.py
"""
Code quality gates and validation system.

This module provides comprehensive code quality validation including:
- Static analysis (pyright, ruff)
- Test coverage validation
- Security scanning
- Performance benchmarks
- Documentation validation
- Code style enforcement
"""

from .exceptions import (
    QualityGateError,
    QualityGateFailureError,
    ValidationError,
)
from .gates import (
    QualityGate,
    QualityGateConfig,
    QualityGateManager,
    QualityGateResult,
    QualityGateStatus,
)
from .reports import (
    QualityReport,
    QualityReportFormatter,
    QualityReportGenerator,
)
from .validators import (
    DocumentationValidator,
    PerformanceValidator,
    SecurityValidator,
    StaticAnalysisValidator,
    StyleValidator,
    TestCoverageValidator,
)

__all__ = [
    # Core gates
    "QualityGate",
    "QualityGateResult",
    "QualityGateStatus",
    "QualityGateConfig",
    "QualityGateManager",

    # Validators
    "StaticAnalysisValidator",
    "TestCoverageValidator",
    "SecurityValidator",
    "PerformanceValidator",
    "DocumentationValidator",
    "StyleValidator",

    # Reports
    "QualityReport",
    "QualityReportGenerator",
    "QualityReportFormatter",

    # Exceptions
    "QualityGateError",
    "ValidationError",
    "QualityGateFailureError",
]
