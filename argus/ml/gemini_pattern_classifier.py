# argus/ml/gemini_pattern_classifier.py

"""
Gemini pattern classifier for SRE logs.
"""

import json
from typing import Any

from argus.ml.gemini_api_client import GeminiAPIClient, GeminiRequest
from argus.pattern_detector.models import PatternMatch, PatternType, TimeWindow


class GeminiPatternClassifier:
    """Classifies SRE logs into issue patterns using Gemini API."""

    def __init__(
        self,
        api_key: str,
        cost_tracker: Any = None,
        rate_limiter: Any = None,
        config: dict | None = None,
    ) -> None:
        self._classification_count = 0
        self._successful_classifications = 0
        self.confidence_assessment_threshold = (
            config.get("confidence_threshold", 0.7) if config else 0.7
        )
        self.gemini_client = GeminiAPIClient(
            api_key=api_key, cost_tracker=cost_tracker, rate_limiter=rate_limiter
        )

    def _select_model(self, window: TimeWindow, threshold_results: list[dict]) -> str:
        if len(window.logs) > 1000 or len(threshold_results) > 10:
            return "gemini-1.5-pro"
        return "gemini-1.5-flash"

    def _map_pattern_type(self, pattern_str: str) -> str | None:
        mapping = {
            "cascade_failure": PatternType.CASCADE_FAILURE,
            "service_degradation": PatternType.SERVICE_DEGRADATION,
            "traffic_spike": PatternType.TRAFFIC_SPIKE,
            "configuration_issue": PatternType.CONFIGURATION_ISSUE,
            "dependency_failure": PatternType.DEPENDENCY_FAILURE,
            "resource_exhaustion": PatternType.RESOURCE_EXHAUSTION,
            "sporadic_errors": PatternType.SPORADIC_ERRORS,
        }
        return mapping.get(pattern_str)

    def _extract_affected_services(self, pattern_data: dict) -> list[str]:
        analysis = pattern_data.get("affected_services_analysis", {})
        primary = analysis.get("primary")
        secondary = analysis.get("secondary", [])
        services = []
        if primary:
            services.append(primary)
        if isinstance(secondary, list):
            for s in secondary:
                if s not in services:
                    services.append(s)
        return services

    def get_performance_stats(self) -> dict[str, Any]:
        return {
            "total_classifications": self._classification_count,
            "successful_classifications": self._successful_classifications,
            "success_rate_percent": (
                (self._successful_classifications / self._classification_count * 100.0)
                if self._classification_count > 0
                else 0.0
            ),
            "confidence_threshold": self.confidence_assessment_threshold,
        }

    def _build_classification_prompt(
        self,
        window: TimeWindow,
        threshold_results: list[dict],
        historical_context: dict | None = None,
        code_context: dict | None = None,
    ) -> str:
        services = set()
        for log in window.logs:
            if log.service_name:
                services.add(log.service_name)

        prompt = (
            f"TIME WINDOW: start={window.start_time}, duration={window.duration_minutes}m\n"
            f"SERVICE ERRORS: services={', '.join(services)}\n"
            f"THRESHOLD VIOLATIONS: {json.dumps(threshold_results)}\n"
            f"HISTORICAL CONTEXT: {json.dumps(historical_context or {})}\n"
            f"SOURCE CODE CONTEXT: {json.dumps(code_context or {})}\n"
        )
        return prompt

    def _build_confidence_prompt(self, pattern_data: dict, window: TimeWindow) -> str:
        prompt = (
            f"Pattern type: {pattern_data.get('pattern_type')}\n"
            f"Confidence: {pattern_data.get('confidence_score')}\n"
            f"Reasoning: {pattern_data.get('reasoning')}\n"
            f"TIME WINDOW CHARACTERISTICS: log count={len(window.logs)}\n"
        )
        return prompt

    def _build_classification_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "pattern_type": {
                    "type": "string",
                    "enum": [
                        "cascade_failure",
                        "service_degradation",
                        "traffic_spike",
                        "configuration_issue",
                        "dependency_failure",
                        "resource_exhaustion",
                        "sporadic_errors",
                    ],
                },
                "confidence_score": {"type": "number"},
                "reasoning": {"type": "string"},
                "severity_assessment": {"type": "string"},
                "affected_services_analysis": {
                    "type": "object",
                    "properties": {
                        "primary": {"type": "string"},
                        "secondary": {"type": "array", "items": {"type": "string"}},
                    },
                },
                "recommended_actions": {"type": "array", "items": {"type": "string"}},
            },
        }

    def _build_confidence_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "overall_confidence": {"type": "number"},
                "confidence_level": {"type": "string"},
            },
        }

    async def classify_patterns(
        self,
        window: TimeWindow,
        threshold_results: list[dict],
        historical_context: dict | None = None,
        code_context: dict | None = None,
    ) -> list[PatternMatch]:
        self._classification_count += 1
        model = self._select_model(window, threshold_results)
        prompt = self._build_classification_prompt(
            window, threshold_results, historical_context, code_context
        )
        schema = self._build_classification_schema()

        req = GeminiRequest(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            generation_config={"response_mime_type": "application/json", "response_schema": schema},
        )
        resp = await self.gemini_client.generate_content(req)
        if not resp.success:
            return []

        try:
            parsed = json.loads(resp.content)
        except Exception:
            return []

        pattern_str = parsed.get("pattern_type")
        if not isinstance(pattern_str, str):
            return []
        pattern_type_enum = self._map_pattern_type(pattern_str)
        if not pattern_type_enum:
            return []

        confidence = parsed.get("confidence_score", 0.0)
        evidence = {"initial_classification": parsed}

        if confidence < self.confidence_assessment_threshold:
            conf_prompt = self._build_confidence_prompt(parsed, window)
            conf_schema = self._build_confidence_schema()
            conf_req = GeminiRequest(
                model=model,
                messages=[{"role": "user", "content": conf_prompt}],
                generation_config={
                    "response_mime_type": "application/json",
                    "response_schema": conf_schema,
                },
            )
            conf_resp = await self.gemini_client.generate_content(conf_req)
            if conf_resp.success:
                try:
                    conf_parsed = json.loads(conf_resp.content)
                except Exception:
                    conf_parsed = {}

                if conf_parsed:
                    confidence = conf_parsed.get("overall_confidence", confidence)
                    evidence["confidence_assessment"] = conf_parsed

        self._successful_classifications += 1

        severity_assessment = parsed.get("severity_assessment", "LOW")
        priority_map = {
            "CRITICAL": "IMMEDIATE",
            "HIGH": "HIGH",
            "MEDIUM": "MEDIUM",
            "LOW": "LOW",
        }
        remediation_priority = priority_map.get(severity_assessment, "LOW")

        pm = PatternMatch(
            pattern_type=pattern_type_enum,
            confidence_score=confidence,
            primary_service=parsed.get("affected_services_analysis", {}).get("primary"),
            affected_services=self._extract_affected_services(parsed),
            severity_level=severity_assessment,
            evidence=evidence,
            remediation_priority=remediation_priority,
            suggested_actions=parsed.get("recommended_actions", []),
        )
        return [pm]
