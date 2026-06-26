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
    "DocumentationValidator",
    "PerformanceValidator",
    # Core gates
    "QualityGate",
    "QualityGateConfig",
    # Exceptions
    "QualityGateError",
    "QualityGateFailureError",
    "QualityGateManager",
    "QualityGateResult",
    "QualityGateStatus",
    # Reports
    "QualityReport",
    "QualityReportFormatter",
    "QualityReportGenerator",
    "SecurityValidator",
    # Validators
    "StaticAnalysisValidator",
    "StyleValidator",
    "TestCoverageValidator",
    "ValidationError",
]
