# argus/agents/legacy_adapter.py

"""
Legacy adapters for backward compatibility.

This module provides legacy adapter classes that allow existing SRE pipelines
to use the enhanced multi-provider LLM system without any code modifications.
"""

import logging
from typing import Any

from ..analysis_agent import AnalysisAgent
from ..llm.config import LLMConfig
from ..remediation_agent import RemediationAgent
from ..triage_agent import TriageAgent
from .enhanced_analysis_agent import EnhancedAnalysisAgent
from .enhanced_remediation_agent import EnhancedRemediationAgent
from .enhanced_triage_agent import EnhancedTriageAgent

logger = logging.getLogger(__name__)


class LegacyTriageAgentAdapter(TriageAgent):
    """
    Adapter for Legacy Triage Agent that routes requests to EnhancedTriageAgent
    when configured with a multi-provider LLM configuration.
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        triage_model: str,
        llm_config: LLMConfig | None = None,
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.triage_model = triage_model
        self.use_enhanced = llm_config is not None

        if self.use_enhanced:
            logger.info("[LEGACY_ADAPTER] Initializing EnhancedTriageAgent for Triage compatibility")
            self.enhanced_agent = EnhancedTriageAgent(
                llm_config=llm_config,
                agent_name="triage_agent",
            )
        else:
            logger.info("[LEGACY_ADAPTER] Using original VertexAI TriageAgent")
            self.enhanced_agent = None
            super().__init__(
                project_id=project_id,
                location=location,
                triage_model=triage_model,
            )

    async def analyze_logs(self, logs: list[str], flow_id: str) -> Any:
        if self.use_enhanced and self.enhanced_agent:
            return await self.enhanced_agent.analyze_logs(logs, flow_id)
        return await super().analyze_logs(logs, flow_id)


class LegacyAnalysisAgentAdapter(AnalysisAgent):
    """
    Adapter for Legacy Analysis Agent that routes requests to EnhancedAnalysisAgent
    when configured with a multi-provider LLM configuration.
    """

    def __init__(
        self,
        project_id: str,
        location: str,
        analysis_model: str,
        llm_config: LLMConfig | None = None,
    ) -> None:
        self.project_id = project_id
        self.location = location
        self.analysis_model = analysis_model
        self.use_enhanced = llm_config is not None

        if self.use_enhanced:
            logger.info("[LEGACY_ADAPTER] Initializing EnhancedAnalysisAgent for Analysis compatibility")
            self.enhanced_agent = EnhancedAnalysisAgent(
                llm_config=llm_config,
                agent_name="analysis_agent",
            )
        else:
            logger.info("[LEGACY_ADAPTER] Using original VertexAI AnalysisAgent")
            self.enhanced_agent = None
            super().__init__(
                project_id=project_id,
                location=location,
                analysis_model=analysis_model,
            )

    async def analyze_issue(
        self,
        triage_packet: Any,
        historical_logs: list[str],
        configs: dict[str, str],
        flow_id: str,
    ) -> Any:
        if self.use_enhanced and self.enhanced_agent:
            if hasattr(triage_packet, "model_dump"):
                triage_data = triage_packet.model_dump()
            elif hasattr(triage_packet, "__dict__"):
                triage_data = {
                    "issue_id": getattr(triage_packet, "issue_id", "unknown"),
                    "severity": getattr(triage_packet, "severity", "medium"),
                    "description": getattr(triage_packet, "description", ""),
                    "natural_language_summary": getattr(triage_packet, "description", ""),
                }
            elif isinstance(triage_packet, dict):
                triage_data = triage_packet
            else:
                triage_data = {}
            return await self.enhanced_agent.analyze_issue(
                triage_data, historical_logs, configs, flow_id
            )
        return super().analyze_issue(triage_packet, historical_logs, configs, flow_id)


class LegacyRemediationAgentAdapter(RemediationAgent):
    """
    Adapter for Legacy Remediation Agent that routes requests to EnhancedRemediationAgent
    when configured with a multi-provider LLM configuration.
    """

    def __init__(
        self,
        github_token: str,
        repo_name: str,
        use_local_patches: bool = False,
        patch_dir: str = "/tmp/real_patches",
        llm_config: LLMConfig | None = None,
    ) -> None:
        self.github_token = github_token
        self.repo_name = repo_name
        self.use_local_patches = use_local_patches
        self.patch_dir = patch_dir
        self.use_enhanced = llm_config is not None

        if self.use_enhanced:
            logger.info("[LEGACY_ADAPTER] Initializing EnhancedRemediationAgent for Remediation compatibility")
            self.enhanced_agent = EnhancedRemediationAgent(
                llm_config=llm_config,
                github_token=github_token,
                repo_name=repo_name,
                use_local_patches=use_local_patches,
                patch_dir=patch_dir,
                agent_name="remediation_agent",
            )
        else:
            logger.info("[LEGACY_ADAPTER] Using original RemediationAgent")
            self.enhanced_agent = None
            super().__init__(
                github_token=github_token,
                repo_name=repo_name,
                use_local_patches=use_local_patches,
                patch_dir=patch_dir,
            )

    async def create_pull_request(
        self,
        remediation_plan: Any,
        branch_name: str,
        base_branch: str,
        flow_id: str,
        issue_id: str,
    ) -> str:
        if self.use_enhanced and self.enhanced_agent:
            return await self.enhanced_agent.create_pull_request(
                remediation_plan, branch_name, base_branch, flow_id, issue_id
            )
        return await super().create_pull_request(
            remediation_plan, branch_name, base_branch, flow_id, issue_id
        )
