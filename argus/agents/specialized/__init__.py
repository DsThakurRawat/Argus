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

# argus/agents/specialized/__init__.py

"""
Enhanced Specialized Agent Classes with Multi-Provider Support.

This module provides enhanced specialized agent classes that inherit from
EnhancedBaseAgent and are tailored for specific types of tasks with
intelligent model selection and multi-provider capabilities.
"""

from .analysis_agent import EnhancedAnalysisAgent
from .code_agent import EnhancedCodeAgent
from .remediation_agent import (
    EnhancedRemediationAgent,
    EnhancedRemediationAgentV2,
)
from .text_agent import EnhancedTextAgent
from .triage_agent import EnhancedTriageAgent

__all__ = [
    "EnhancedAnalysisAgent",
    "EnhancedCodeAgent",
    "EnhancedRemediationAgent",
    "EnhancedRemediationAgentV2",
    "EnhancedTextAgent",
    "EnhancedTriageAgent",
]
