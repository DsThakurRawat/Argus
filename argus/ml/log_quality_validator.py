#

"""
Log quality validator checking log completeness, noise, consistency, and duplicates.
"""

from collections import Counter
import re
from typing import Any

from .validation_config import (
    LogEntry,
    QualityThresholds,
    TimeWindow,
    ValidationMetrics,
    ValidationRules,
)


class LogQualityValidator:
    """Pre-processing validator ensuring high-quality input for AI analysis."""

    def __init__(self, thresholds: QualityThresholds | None = None) -> None:
        self.thresholds = thresholds or QualityThresholds()

    def _extract_message_pattern(self, message: str) -> str:
        """Extracts and normalizes a log message into a general pattern."""
        if not message:
            return ""
        # IP Address placeholder
        pattern = re.sub(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", "IP", message)
        # Hex IDs (8+ chars) placeholder
        pattern = re.sub(r"\b[a-fA-F0-9]{8,}\b", "ID", pattern)
        # Numbers placeholder
        pattern = re.sub(r"\b\d+\b", "N", pattern)
        return pattern

    def _is_noisy_log(self, log: LogEntry) -> bool:
        """Checks if log entry is considered noise."""
        return (
            ValidationRules.is_noisy_severity(log.severity)
            or ValidationRules.is_message_too_short(log.error_message)
        )

    def assess_log_quality(self, window: TimeWindow) -> dict[str, Any]:
        """Calculates completeness, noise ratio, consistency, and duplicates."""
        if not window.logs:
            return ValidationMetrics.empty_metrics()

        total = len(window.logs)

        # 1. Completeness
        complete_count = sum(
            1 for log in window.logs if ValidationRules.is_essential_field_complete(log)
        )
        completeness = complete_count / total

        # 2. Noise ratio
        noisy_count = sum(1 for log in window.logs if self._is_noisy_log(log))
        noise_ratio = noisy_count / total

        # 3. Consistency
        patterns = [self._extract_message_pattern(log.error_message) for log in window.logs]
        if patterns:
            pattern_counts = Counter(patterns)
            most_frequent_count = pattern_counts.most_common(1)[0][1]
            consistency = most_frequent_count / total
        else:
            consistency = 0.0

        # 4. Duplicate ratio
        messages = [log.error_message for log in window.logs if log.error_message is not None]
        unique_messages_count = len(set(messages))
        if total > 0:
            # duplicate ratio = (total - unique_messages) / total
            # if we have no messages at all, treat duplicate ratio as 0 or 1? Let's check test assertions
            duplicate_ratio = max(0.0, (total - unique_messages_count) / total)
        else:
            duplicate_ratio = 0.0

        # Calculate quality factors
        low_noise = 1.0 - noise_ratio
        low_duplicates = 1.0 - duplicate_ratio
        overall_quality = (completeness + low_noise + consistency + low_duplicates) / 4

        # Validate against thresholds
        passes_threshold = (
            completeness >= self.thresholds.min_completeness
            and noise_ratio <= self.thresholds.max_noise_ratio
            and consistency >= self.thresholds.min_consistency
            and duplicate_ratio <= self.thresholds.max_duplicate_ratio
            and overall_quality >= self.thresholds.overall_quality_threshold
        )

        return {
            "completeness": completeness,
            "noise_ratio": noise_ratio,
            "consistency": consistency,
            "duplicate_ratio": duplicate_ratio,
            "passes_threshold": passes_threshold,
            "total_logs_analyzed": total,
            "overall_quality": overall_quality,
            "quality_factors": {
                "completeness": completeness,
                "low_noise": low_noise,
                "consistency": consistency,
                "low_duplicates": low_duplicates,
            },
        }

    def validate_for_processing(self, window: TimeWindow) -> bool:
        """Returns True if the window passes all quality thresholds."""
        return self.assess_log_quality(window)["passes_threshold"]

    def get_quality_recommendations(self, metrics: dict[str, Any]) -> list[str]:
        """Provides actionable recommendations based on quality metrics."""
        recommendations = []

        if metrics["completeness"] < self.thresholds.min_completeness:
            recommendations.append(
                "Ensure essential fields service_name, error_message, and severity are populated to improve completeness."
            )

        if metrics["noise_ratio"] > self.thresholds.max_noise_ratio:
            recommendations.append(
                "Filter out DEBUG/TRACE level logs and extremely short/empty messages to reduce noise."
            )

        if metrics["consistency"] < self.thresholds.min_consistency:
            recommendations.append(
                "standardize log formats across services to improve pattern consistency."
            )

        if metrics["duplicate_ratio"] > self.thresholds.max_duplicate_ratio:
            recommendations.append(
                "Apply deduplication or rate limiting to reduce duplicate error messages."
            )

        if not recommendations:
            recommendations.append("Log quality is excellent and meets all thresholds.")

        return recommendations
