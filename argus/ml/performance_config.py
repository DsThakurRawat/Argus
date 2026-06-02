#

"""
Performance configuration, drift alert, and metrics definitions.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class DriftAlert:
    """Drift alert dataclass recording baseline, current, and severity details."""

    drift_type: str
    severity: str  # "HIGH", "MEDIUM", "LOW"
    baseline_value: float
    current_value: float
    drift_amount: float
    timestamp: datetime

    def __str__(self) -> str:
        return (
            f"{self.drift_type.upper()}({self.severity}): "
            f"baseline={self.baseline_value:.3f}, "
            f"current={self.current_value:.3f}, "
            f"drift={self.drift_amount:.3f}"
        )


@dataclass
class PerformanceConfig:
    """Configuration options for model performance monitoring and drift checking."""

    window_size: int = 100
    recent_window_size: int = 25
    baseline_establishment_size: int = 20
    accuracy_drift_threshold: float = 0.15
    confidence_drift_threshold: float = 0.20
    latency_drift_multiplier: float = 2.0
    pattern_accuracy_window: int = 10
    max_pattern_history: int = 100
    high_drift_threshold: float = 0.25
    drift_check_interval_seconds: int = 3600
    min_samples_for_drift_check: int = 50


class PerformanceMetrics:
    """Utility methods for calculating performance metrics and categorizing drift."""

    @staticmethod
    def empty_metrics() -> dict[str, Any]:
        """Returns default empty performance metrics."""
        return {
            "overall_accuracy": 0.0,
            "baseline_accuracy": None,
            "total_predictions": 0,
            "baseline_established": False,
        }

    @staticmethod
    def calculate_drift_percentage(baseline: float, current: float) -> float:
        """Calculates percentage change of current against baseline."""
        if baseline == 0.0:
            return 0.0
        return ((current - baseline) / baseline) * 100

    @staticmethod
    def is_significant_drift(baseline: float, current: float, threshold: float) -> bool:
        """Returns True if absolute drift exceeds threshold."""
        return abs(baseline - current) > threshold

    @staticmethod
    def categorize_drift_severity(drift_amount: float, high_threshold: float) -> str:
        """Determines severity label based on drift ratio to high threshold."""
        if drift_amount > high_threshold:
            return "HIGH"
        elif drift_amount > high_threshold * 0.5:
            return "MEDIUM"
        else:
            return "LOW"
