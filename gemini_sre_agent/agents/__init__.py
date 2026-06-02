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

# gemini_sre_agent/agents/__init__.py

"""
Enhanced agent base classes with structured output support.

This module provides the foundation for all agents in the system, including
structured output capabilities, primary/fallback model logic, and integration
with Mirascope for prompt management. Now includes multi-provider support.
"""

from .base import AgentStats, BaseAgent
from .enhanced_base import EnhancedBaseAgent
from .enhanced_specialized import (
    EnhancedAnalysisAgent,
    EnhancedCodeAgent,
    EnhancedRemediationAgent,
    EnhancedTextAgent,
    EnhancedTriageAgent,
)
from .response_models import AnalysisResult, CodeResponse, TextResponse
from .specialized.analysis_agent import EnhancedAnalysisAgent
from .specialized.code_agent import EnhancedCodeAgent
from .specialized.text_agent import EnhancedTextAgent

__all__ = [
    # Base agents
    "BaseAgent",
    "AgentStats",
    "TextResponse",
    "AnalysisResult",
    "CodeResponse",
    "EnhancedTextAgent",
    "EnhancedAnalysisAgent",
    "EnhancedCodeAgent",
    # Enhanced agents (multi-provider support)
    "EnhancedBaseAgent",
    "EnhancedTriageAgent",
    "EnhancedRemediationAgent",
]
