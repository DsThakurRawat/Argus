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
Validation configuration and model definitions for log quality.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class LogEntry:
    """Represents a single parsed log entry for quality validation."""

    timestamp: datetime
    service_name: str | None = None
    error_message: str | None = None
    severity: str | None = None
    trace_id: str | None = None
    span_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.metadata is None:
            self.metadata = {}


@dataclass
class QualityThresholds:
    """Configurable quality validation thresholds."""

    min_completeness: float = 0.80
    max_noise_ratio: float = 0.20
    min_consistency: float = 0.70
    max_duplicate_ratio: float = 0.30
    overall_quality_threshold: float = 0.75


@dataclass
class TimeWindow:
    """A collection of logs over a specific time window."""

    start_time: datetime
    end_time: datetime
    logs: list[LogEntry]

    def __post_init__(self) -> None:
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")

    @property
    def duration_seconds(self) -> float:
        """Returns the duration of the time window in seconds."""
        return (self.end_time - self.start_time).total_seconds()

    @property
    def log_count(self) -> int:
        """Returns the number of logs in the window."""
        return len(self.logs)


class ValidationMetrics:
    """Helper utilities for formatting and generating empty validation metrics."""

    @staticmethod
    def empty_metrics() -> dict[str, Any]:
        """Returns default empty metrics dictionary."""
        return {
            "completeness": 0.0,
            "noise_ratio": 1.0,
            "consistency": 0.0,
            "duplicate_ratio": 0.0,
            "passes_threshold": False,
            "total_logs_analyzed": 0,
            "overall_quality": 0.0,
            "quality_factors": {
                "completeness": 0.0,
                "low_noise": 0.0,
                "consistency": 0.0,
                "low_duplicates": 0.0,
            },
        }

    @staticmethod
    def format_quality_score(score: float) -> str:
        """Formats score float as percentage string."""
        return f"{score * 100:.1f}%"

    @staticmethod
    def categorize_quality_level(score: float) -> str:
        """Categorizes score into descriptive level string."""
        if score >= 0.90:
            return "EXCELLENT"
        elif score >= 0.80:
            return "GOOD"
        elif score >= 0.70:
            return "FAIR"
        elif score >= 0.50:
            return "POOR"
        else:
            return "CRITICAL"


class ValidationRules:
    """Rules defining essential fields, noise, and short logs."""

    @staticmethod
    def is_essential_field_complete(log: LogEntry) -> bool:
        """Checks if all essential fields are non-empty."""
        return bool(log.service_name and log.error_message and log.severity)

    @staticmethod
    def is_noisy_severity(severity: str | None) -> bool:
        """Checks if severity is noisy (e.g. DEBUG, TRACE)."""
        if not severity:
            return False
        return severity.upper() in ("DEBUG", "TRACE")

    @staticmethod
    def is_message_too_short(message: str | None) -> bool:
        """Checks if message is too short (less than 10 characters)."""
        if not message:
            return True
        return len(message) < 10
