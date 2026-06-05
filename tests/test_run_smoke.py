import pytest
import tempfile
import asyncio
from pathlib import Path
from argus.ingestion.interfaces.core import LogEntry
from main import run_pipeline

@pytest.mark.asyncio
async def test_smoke_pipeline():
    """Smoke test to verify that the CLI pipeline runs successfully without crashing."""
    from datetime import datetime
    import os
    from argus.ingestion.interfaces.core import LogSeverity
    os.environ["GEMINI_API_KEY"] = "mock_key"
    os.environ["OPENAI_API_KEY"] = "mock_key"
    mock_log = LogEntry(
        id="MOCK-LOG-1",
        timestamp=datetime.now(),
        severity=LogSeverity.ERROR,
        message="Connection timeout connecting to database",
        source="db-service"
    )
    
    from unittest.mock import patch, AsyncMock
    from argus.triage_agent import TriagePacket
    from argus.agents.agent_models import RemediationPlan, AnalysisResult, AnalysisFinding, RemediationStep
    
    mock_triage = TriagePacket(
        issue_id="mock",
        initial_timestamp="2026-06-05T00:00:00Z",
        detected_pattern="mock_pattern",
        preliminary_severity_score=8,
        affected_services=[],
        sample_log_entries=[],
        natural_language_summary="mock summary",
    )
    mock_analysis = AnalysisResult(
        workflow_id="mock",
        analysis_id="mock",
        analysis_type="mock",
        timestamp=0,
        detected_patterns=[],
        insights=[],
        recommendations=[],
        confidence_score=1.0,
        analysis_duration=0.0,
        patterns_analyzed=0,
        success=True,
        summary="mock summary",
        key_findings=[AnalysisFinding(title="mock title", category="performance", description="mock finding", severity="high", confidence=1.0)],
        overall_severity="high",
        overall_confidence=1.0,
        risk_assessment="mock risk",
        business_impact="mock impact",
        next_steps=["mock step"],
    )
    mock_remed = RemediationPlan(
        plan_name="mock plan",
        issue_description="mock issue",
        priority="high",
        steps=[RemediationStep(
            order=1, 
            title="mock title", 
            description="mock desc", 
            action_type="immediate", 
            risk_level="low",
            commands=["mock command"]
        )],
        success_criteria=["mock criteria"],
        risk_assessment="mock risk",
    )

    from unittest.mock import MagicMock
    mock_config = MagicMock()

    with patch('argus.agents.enhanced_specialized.EnhancedTriageAgent.triage_issue', new_callable=AsyncMock, return_value=mock_triage), \
         patch('argus.agents.enhanced_specialized.EnhancedAnalysisAgent.analyze', new_callable=AsyncMock, return_value=mock_analysis), \
         patch('argus.agents.enhanced_specialized.EnhancedRemediationAgentV2.create_remediation_plan', new_callable=AsyncMock, return_value=mock_remed), \
         patch('argus.llm.config_manager.ConfigManager.get_config', return_value=mock_config):
         
        packet = await run_pipeline(mock_log_entry=mock_log)
    
    assert packet is not None
    # The triage packet should have parsed our mock log.
    assert hasattr(packet, "issue_id") or "issue_id" in packet
