#

"""
Model performance monitor class tracking accuracy, latency, confidence, and pattern metrics.
"""

from collections import defaultdict
from datetime import datetime
from typing import Any

from .drift_detector import DriftDetector, MetricsCalculator
from .performance_config import DriftAlert, PerformanceConfig, PerformanceMetrics


class ModelPerformanceMonitor:
    """Monitors model prediction accuracy, confidence, and latency over time to detect drift."""

    def __init__(self, config: PerformanceConfig | None = None) -> None:
        self.config = config or PerformanceConfig()
        self.accuracy_history: list[float] = []
        self.confidence_history: list[float] = []
        self.latency_history: list[float] = []
        self.pattern_type_accuracy: dict[str, list[float]] = defaultdict(list)

        self.baseline_accuracy: float | None = None
        self.baseline_confidence: float | None = None
        self.baseline_latency: float | None = None

        self.drift_alerts: list[DriftAlert] = []
        self.drift_detector = DriftDetector(self.config)
        self.last_drift_check = datetime.now()

    def _trim_pattern_history(self, pattern: str) -> None:
        """Trims pattern history list to configured max size."""
        self.pattern_type_accuracy[pattern] = MetricsCalculator.trim_history(
            self.pattern_type_accuracy[pattern], self.config.max_pattern_history
        )

    def _calculate_pattern_accuracy(self) -> dict[str, dict[str, Any]]:
        """Calculates accuracy summary for all tracked pattern types."""
        result = {}
        for pattern, accuracies in self.pattern_type_accuracy.items():
            result[pattern] = MetricsCalculator.calculate_pattern_accuracy(
                accuracies, self.config.pattern_accuracy_window
            )
        return result

    def _should_check_drift(self) -> bool:
        """Returns True if the time elapsed since the last check exceeds the interval."""
        elapsed = (datetime.now() - self.last_drift_check).total_seconds()
        return elapsed >= self.config.drift_check_interval_seconds

    def _can_check_drift(self) -> bool:
        """Returns True if baseline is set and minimum samples are met."""
        return (
            self.baseline_accuracy is not None
            and len(self.accuracy_history) >= self.config.min_samples_for_drift_check
        )

    async def track_prediction_accuracy(
        self,
        prediction: str,
        actual_outcome: str,
        confidence_score: float,
        latency_ms: float,
    ) -> None:
        """Tracks a new prediction and checks for baseline establishment or drift alerts."""
        is_correct = 1.0 if prediction == actual_outcome else 0.0

        self.accuracy_history.append(is_correct)
        self.confidence_history.append(confidence_score)
        self.latency_history.append(latency_ms)
        self.pattern_type_accuracy[prediction].append(is_correct)

        # Trim rolling windows
        self.accuracy_history = MetricsCalculator.trim_history(
            self.accuracy_history, self.config.window_size
        )
        self.confidence_history = MetricsCalculator.trim_history(
            self.confidence_history, self.config.window_size
        )
        self.latency_history = MetricsCalculator.trim_history(
            self.latency_history, self.config.window_size
        )
        self._trim_pattern_history(prediction)

        # Baseline establishment
        if (
            self.baseline_accuracy is None
            and len(self.accuracy_history) >= self.config.baseline_establishment_size
        ) or (
            self.baseline_accuracy is None
            and len(self.accuracy_history) >= self.config.baseline_establishment_size
        ):
            # Calculate mean using the establishment size
            est_size = self.config.baseline_establishment_size
            self.baseline_accuracy = sum(self.accuracy_history[:est_size]) / est_size
            self.baseline_confidence = sum(self.confidence_history[:est_size]) / est_size
            self.baseline_latency = sum(self.latency_history[:est_size]) / est_size

        # Drift checking
        if self._should_check_drift() and self._can_check_drift():
            recent_acc = MetricsCalculator.calculate_recent_metrics(
                self.accuracy_history, self.config.recent_window_size
            )
            recent_conf = MetricsCalculator.calculate_recent_metrics(
                self.confidence_history, self.config.recent_window_size
            )
            recent_lat = MetricsCalculator.calculate_recent_metrics(
                self.latency_history, self.config.recent_window_size
            )

            await self.drift_detector.check_accuracy_drift(
                recent_acc, self.baseline_accuracy, self.drift_alerts
            )
            await self.drift_detector.check_confidence_drift(
                recent_conf, self.baseline_confidence, self.drift_alerts
            )
            await self.drift_detector.check_latency_drift(
                recent_lat, self.baseline_latency, self.drift_alerts
            )

            self.last_drift_check = datetime.now()

    def get_performance_metrics(self) -> dict[str, Any]:
        """Returns current performance metrics dashboard dict."""
        if not self.accuracy_history:
            return PerformanceMetrics.empty_metrics()

        total = len(self.accuracy_history)
        overall_accuracy = sum(self.accuracy_history) / total

        return {
            "overall_accuracy": overall_accuracy,
            "baseline_accuracy": self.baseline_accuracy,
            "baseline_confidence": self.baseline_confidence,
            "baseline_latency": self.baseline_latency,
            "total_predictions": total,
            "baseline_established": self.baseline_accuracy is not None,
            "drift_check_enabled": self._can_check_drift(),
            "pattern_accuracy": self._calculate_pattern_accuracy(),
        }

    def get_drift_summary(self) -> dict[str, Any]:
        """Returns summarized drift statistics and severity counts."""
        return MetricsCalculator.analyze_drift_alerts(self.drift_alerts)

    def reset_drift_alerts(self) -> int:
        """Clears all accumulated drift alerts and returns cleared count."""
        cleared = len(self.drift_alerts)
        self.drift_alerts = []
        return cleared
