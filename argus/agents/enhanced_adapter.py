# Copyright 2026 divyanshrawat
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

"""Enhanced Agent Adapters and Migration Helpers."""

import logging
from typing import Any, cast

from ..llm.config import LLMConfig
from .enhanced_specialized import (
    EnhancedAnalysisAgent,
    EnhancedCodeAgent,
    EnhancedRemediationAgent,
    EnhancedTextAgent,
    EnhancedTriageAgent,
)

logger = logging.getLogger(__name__)


class EnhancedAgentAdapter:
    """Adapter to wrap legacy agents and add enhanced multi-provider features."""

    def __init__(
        self,
        legacy_agent: Any,
        llm_config: LLMConfig,
        enable_enhancements: bool = True,
    ) -> None:
        self.legacy_agent = legacy_agent
        self.llm_config = llm_config
        self.enable_enhancements = enable_enhancements
        self._enhanced_agent = None

        if self.enable_enhancements:
            self._init_enhanced_agent()

    def _init_enhanced_agent(self) -> None:
        legacy_class_name = self.legacy_agent.__class__.__name__
        primary_model = getattr(self.legacy_agent, "primary_model", None)
        fallback_model = getattr(self.legacy_agent, "fallback_model", None)
        max_retries = getattr(self.legacy_agent, "max_retries", 2)
        collect_stats = getattr(self.legacy_agent, "collect_stats", True)

        kwargs = {
            "llm_config": self.llm_config,
            "primary_model": primary_model,
            "fallback_model": fallback_model,
            "max_retries": max_retries,
            "collect_stats": collect_stats,
        }

        # Filter out None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if legacy_class_name == "TextAgent":
            self._enhanced_agent = EnhancedTextAgent(**kwargs)
        elif legacy_class_name == "TriageAgent":
            self._enhanced_agent = EnhancedTriageAgent(**kwargs)
        elif legacy_class_name == "AnalysisAgent":
            self._enhanced_agent = EnhancedAnalysisAgent(**kwargs)
        elif legacy_class_name == "CodeAgent":
            self._enhanced_agent = EnhancedCodeAgent(**kwargs)
        elif legacy_class_name == "RemediationAgent":
            github_token = getattr(self.legacy_agent, "github_token", "dummy_token")
            repo_name = getattr(self.legacy_agent, "repo_name", "dummy_repo")
            self._enhanced_agent = EnhancedRemediationAgent(
                github_token=github_token,
                repo_name=repo_name,
                **kwargs
            )
        else:
            self._enhanced_agent = EnhancedTextAgent(**kwargs)

    def enable_enhanced_features(self) -> None:
        """Enable enhanced multi-provider features."""
        self.enable_enhancements = True
        if not self._enhanced_agent:
            self._init_enhanced_agent()

    def disable_enhanced_features(self) -> None:
        """Disable enhanced multi-provider features and use legacy."""
        self.enable_enhancements = False

    async def execute(self, prompt_name: str, prompt_args: dict[str, Any]) -> Any:
        """Execute request using either legacy or enhanced agent."""
        if self.enable_enhancements and self._enhanced_agent:
            return await self._enhanced_agent.execute(prompt_name, prompt_args)
        return await self.legacy_agent.execute(prompt_name, prompt_args)


class AgentMigrationHelper:
    """Helper utilities for migrating legacy agents to enhanced agents."""

    @staticmethod
    def create_enhanced_agent_from_legacy(legacy_agent: Any, llm_config: LLMConfig) -> Any:
        """Create a fully-configured enhanced agent instance from a legacy agent."""
        legacy_class_name = legacy_agent.__class__.__name__
        primary_model = getattr(legacy_agent, "primary_model", None)
        fallback_model = getattr(legacy_agent, "fallback_model", None)
        max_retries = getattr(legacy_agent, "max_retries", 2)
        collect_stats = getattr(legacy_agent, "collect_stats", True)

        kwargs = {
            "llm_config": llm_config,
            "primary_model": primary_model,
            "fallback_model": fallback_model,
            "max_retries": max_retries,
            "collect_stats": collect_stats,
        }

        # Filter out None values
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        if legacy_class_name == "TextAgent":
            return EnhancedTextAgent(**kwargs)
        elif legacy_class_name == "TriageAgent":
            return EnhancedTriageAgent(**kwargs)
        elif legacy_class_name == "AnalysisAgent":
            return EnhancedAnalysisAgent(**kwargs)
        elif legacy_class_name == "CodeAgent":
            return EnhancedCodeAgent(**kwargs)
        elif legacy_class_name == "RemediationAgent":
            github_token = getattr(legacy_agent, "github_token", "dummy_token")
            repo_name = getattr(legacy_agent, "repo_name", "dummy_repo")
            return EnhancedRemediationAgent(
                github_token=github_token,
                repo_name=repo_name,
                **kwargs
            )
        else:
            return EnhancedTextAgent(**kwargs)

    @staticmethod
    def validate_migration_compatibility(legacy_agent: Any, llm_config: LLMConfig) -> dict[str, Any]:
        """Validate if a legacy agent is compatible for migration."""
        required_attrs = ["response_model", "llm_service", "_prompts"]
        missing = []
        is_mock = hasattr(legacy_agent, "_mock_name") or hasattr(legacy_agent, "mock_add_spec")

        for attr in required_attrs:
            if is_mock:
                if attr not in legacy_agent.__dict__:
                    missing.append(attr)
            else:
                if not hasattr(legacy_agent, attr):
                    missing.append(attr)

        compatible = len(missing) == 0
        return {
            "compatible": compatible,
            "required_changes": [f"Missing attribute: {attr}" for attr in missing],
        }

    @staticmethod
    def generate_migration_report(agents: list[Any], llm_config: LLMConfig) -> dict[str, Any]:
        """Generate a migration compatibility report for a list of legacy agents."""
        report: dict[str, Any] = {
            "total_agents": len(agents),
            "compatible_agents": 0,
            "incompatible_agents": 0,
            "agent_details": [],
            "overall_recommendations": [],
        }

        for agent in agents:
            compat_result = AgentMigrationHelper.validate_migration_compatibility(agent, llm_config)
            agent_info = {
                "name": agent.__class__.__name__,
                "compatible": compat_result["compatible"],
                "required_changes": compat_result["required_changes"],
            }
            report["agent_details"].append(agent_info)

            if compat_result["compatible"]:
                report["compatible_agents"] += 1
            else:
                report["incompatible_agents"] += 1

        if report["incompatible_agents"] > 0:
            report["overall_recommendations"].append(
                "Ensure all legacy agents inherit from BaseAgent and initialize required fields."
            )
        else:
            report["overall_recommendations"].append("All agents are ready for migration.")

        return report


class BackwardCompatibilityWrapper:
    """Wrapper that exposes legacy agent attributes on top of an enhanced agent."""

    def __init__(self, enhanced_agent: Any) -> None:
        self._enhanced_agent = enhanced_agent

    def __getattr__(self, name: str) -> Any:
        return getattr(self._enhanced_agent, name)

    async def execute(self, prompt_name: str, prompt_args: dict[str, Any]) -> Any:
        """Execute request via the underlying enhanced agent."""
        return await self._enhanced_agent.execute(prompt_name, prompt_args)

    def get_stats_summary(self) -> dict[str, Any]:
        """Get performance statistics from the underlying enhanced agent."""
        return self._enhanced_agent.get_stats_summary()
