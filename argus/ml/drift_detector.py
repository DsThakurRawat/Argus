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
Drift detector and metric calculation helper utilities.
"""

from datetime import datetime
from typing import Any

from .performance_config import DriftAlert, PerformanceConfig, PerformanceMetrics


class MetricsCalculator:
    """Helper class for calculations on rolling performance history windows."""

    @staticmethod
    def calculate_recent_metrics(history: list[float], window: int) -> float:
        """Returns the mean value of the last window items in history."""
        if not history:
            return 0.0
        recent = history[-window:]
        return round(sum(recent) / len(recent), 7)

    @staticmethod
    def calculate_pattern_accuracy(
        accuracies: list[float], recent_samples: int
    ) -> dict[str, Any]:
        """Calculates accuracy metric summary for specific pattern histories."""
        total_samples = len(accuracies)
        if not accuracies:
            return {"accuracy": 0.0, "sample_count": 0, "recent_samples": 0}
        recent = accuracies[-recent_samples:]
        acc = round(sum(recent) / len(recent), 7)
        return {
            "accuracy": acc,
            "sample_count": total_samples,
            "recent_samples": len(recent),
        }

    @staticmethod
    def trim_history(history: list[Any], max_size: int) -> list[Any]:
        """Trims history list to keep only the last max_size items."""
        return history[-max_size:]

    @staticmethod
    def analyze_drift_alerts(alerts: list[DriftAlert]) -> dict[str, Any]:
        """Summarizes severity counts and presence of drift alerts."""
        if not alerts:
            return {
                "has_drift": False,
                "total_alerts": 0,
                "recent_alerts": [],
                "severity_counts": {"HIGH": 0, "MEDIUM": 0, "LOW": 0},
            }

        severity_counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        high_severity_recent = 0

        for alert in alerts:
            severity = alert.severity.upper()
            if severity in severity_counts:
                severity_counts[severity] += 1
            if severity in ("HIGH", "MEDIUM"):
                high_severity_recent += 1

        return {
            "has_drift": True,
            "total_alerts": len(alerts),
            "recent_alerts": alerts,
            "severity_counts": severity_counts,
            "high_severity_recent": high_severity_recent,
        }


class DriftDetector:
    """Detects metric drifts based on accuracy, confidence, and latency limits."""

    def __init__(self, config: PerformanceConfig) -> None:
        self.config = config

    def _determine_drift_severity(self, drift_amount: float, high_threshold: float) -> str:
        """Determines severity categorization based on configured threshold."""
        return PerformanceMetrics.categorize_drift_severity(drift_amount, high_threshold)

    async def check_accuracy_drift(
        self, current: float, baseline: float | None, alerts: list[DriftAlert]
    ) -> None:
        """Checks accuracy metrics against baseline and generates DriftAlert if drift exceeds threshold."""
        if baseline is None:
            return

        if PerformanceMetrics.is_significant_drift(
            baseline, current, self.config.accuracy_drift_threshold
        ):
            drift_amount = abs(baseline - current)
            severity = self._determine_drift_severity(
                drift_amount, self.config.high_drift_threshold
            )
            alerts.append(
                DriftAlert(
                    drift_type="accuracy_drift",
                    severity=severity,
                    baseline_value=baseline,
                    current_value=current,
                    drift_amount=drift_amount,
                    timestamp=datetime.now(),
                )
            )

    async def check_confidence_drift(
        self, current: float, baseline: float | None, alerts: list[DriftAlert]
    ) -> None:
        """Checks confidence metrics against baseline and generates DriftAlert if drift exceeds threshold."""
        if baseline is None:
            return

        if PerformanceMetrics.is_significant_drift(
            baseline, current, self.config.confidence_drift_threshold
        ):
            drift_amount = abs(baseline - current)
            severity = self._determine_drift_severity(
                drift_amount, self.config.high_drift_threshold
            )
            alerts.append(
                DriftAlert(
                    drift_type="confidence_drift",
                    severity=severity,
                    baseline_value=baseline,
                    current_value=current,
                    drift_amount=drift_amount,
                    timestamp=datetime.now(),
                )
            )

    async def check_latency_drift(
        self, current: float, baseline: float | None, alerts: list[DriftAlert]
    ) -> None:
        """Checks latency metrics against baseline and generates DriftAlert if latency degrades beyond multiplier."""
        if baseline is None:
            return

        threshold = baseline * self.config.latency_drift_multiplier
        if current > threshold:
            drift_amount = current - baseline
            severity = self._determine_drift_severity(drift_amount, threshold)
            alerts.append(
                DriftAlert(
                    drift_type="latency_drift",
                    severity=severity,
                    baseline_value=baseline,
                    current_value=current,
                    drift_amount=drift_amount,
                    timestamp=datetime.now(),
                )
            )
