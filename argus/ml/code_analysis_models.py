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

"""
Data models representing configuration and metrics for codebase analysis.
"""

from dataclasses import dataclass
from datetime import datetime
import os
from typing import Any


@dataclass
class CodeAnalysisConfig:
    """Configuring codebase context extraction and scan limits."""

    repository_path: str
    enable_static_analysis: bool = False
    enable_complexity_analysis: bool = False
    enable_dependency_scan: bool = False
    analysis_timeout_seconds: int = 30
    max_recent_commits: int = 10

    def __post_init__(self) -> None:
        if self.analysis_timeout_seconds <= 0:
            raise ValueError("analysis_timeout_seconds must be positive")
        if self.max_recent_commits <= 0:
            raise ValueError("max_recent_commits must be positive")
        if not os.path.exists(self.repository_path):
            raise ValueError("Repository path does not exist")


@dataclass
class CodeChange:
    """Represents a code change / commit."""

    commit_hash: str
    timestamp: datetime
    author: str
    message: str
    files_changed: list[str]
    lines_added: int
    lines_deleted: int
    is_rollback: bool = False

    def __post_init__(self) -> None:
        if not self.commit_hash:
            raise ValueError("commit_hash cannot be empty")
        if not self.author:
            raise ValueError("author cannot be empty")
        if self.lines_added < 0:
            raise ValueError("lines_added cannot be negative")
        if self.lines_deleted < 0:
            raise ValueError("lines_deleted cannot be negative")

    @property
    def short_hash(self) -> str:
        """Returns short commit hash."""
        return self.commit_hash[:8]

    @property
    def net_lines_changed(self) -> int:
        """Returns lines added minus lines deleted."""
        return self.lines_added - self.lines_deleted

    @property
    def total_lines_changed(self) -> int:
        """Returns lines added plus lines deleted."""
        return self.lines_added + self.lines_deleted


@dataclass
class StaticAnalysisResult:
    """Findings from static analysis tools."""

    tool_name: str
    findings: list[dict[str, Any]]
    scan_duration_seconds: float
    files_analyzed: list[str]
    error_count: int = 0
    warning_count: int = 0
    info_count: int = 0

    @property
    def total_findings(self) -> int:
        """Returns total findings across all levels."""
        return self.error_count + self.warning_count + self.info_count

    @property
    def has_errors(self) -> bool:
        """Returns True if error count is greater than zero."""
        return self.error_count > 0

    def get_findings_by_severity(self, severity: str) -> list[dict[str, Any]]:
        """Filters findings case-insensitively by severity value."""
        return [
            f
            for f in self.findings
            if f.get("severity", "").strip().lower() == severity.strip().lower()
        ]


@dataclass
class ComplexityMetrics:
    """Complexity metrics including cyclomatic and maintainability ratings."""

    cyclomatic_complexity: float
    cognitive_complexity: float
    maintainability_index: float
    lines_of_code: int
    technical_debt_ratio: float
    code_coverage: float = 0.0

    def __post_init__(self) -> None:
        if self.cyclomatic_complexity < 0:
            raise ValueError("cyclomatic_complexity cannot be negative")
        if not (0.0 <= self.maintainability_index <= 100.0):
            raise ValueError("maintainability_index must be between 0 and 100")
        if not (0.0 <= self.code_coverage <= 100.0):
            raise ValueError("code_coverage must be between 0 and 100")

    @property
    def complexity_rating(self) -> str:
        """Returns complexity rating from Low, Medium, to High."""
        if self.cyclomatic_complexity >= 20.0:
            return "High"
        elif self.cyclomatic_complexity >= 10.0:
            return "Medium"
        else:
            return "Low"

    @property
    def maintainability_rating(self) -> str:
        """Returns maintainability index classification."""
        if self.maintainability_index >= 80.0:
            return "Excellent"
        elif self.maintainability_index >= 65.0:
            return "Good"
        elif self.maintainability_index >= 50.0:
            return "Fair"
        else:
            return "Poor"


@dataclass
class DependencyVulnerability:
    """Known vulnerability in repository dependencies."""

    package_name: str
    current_version: str
    vulnerability_id: str
    severity: str
    description: str
    fixed_version: str | None = None
    cve_id: str | None = None

    def __post_init__(self) -> None:
        if self.severity.upper() not in ("CRITICAL", "HIGH", "MEDIUM", "LOW"):
            raise ValueError("severity must be CRITICAL, HIGH, MEDIUM, or LOW")

    @property
    def is_fixable(self) -> bool:
        """Returns True if a fixed version is available."""
        return bool(self.fixed_version)

    @property
    def severity_score(self) -> int:
        """Numerical score representing severity category."""
        return {"CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}[self.severity.upper()]
