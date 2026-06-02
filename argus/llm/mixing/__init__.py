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

# argus/llm/mixing/__init__.py

"""
Advanced Model Mixing Module.

This module provides sophisticated model mixing capabilities for complex tasks,
including task decomposition, parallel execution, result aggregation, and
context sharing between multiple models.
"""

from .context_sharing import (
    ContextEntry,
    ContextManager,
    ContextPropagator,
    FeedbackLoop,
    SharedContext,
    context_manager,
    context_propagator,
    feedback_loop,
)
from .intelligent_cache import IntelligentCache
from .model_mixer import (
    MixingResult,
    MixingStrategy,
    ModelConfig,
    ModelMixer,
    ResultAggregator,
    SimpleResultAggregator,
    SimpleTaskDecomposer,
    TaskDecomposer,
    TaskDecomposition,
    TaskType,
)

__all__ = [
    # Model mixing
    "MixingStrategy",
    "TaskType",
    "ModelConfig",
    "MixingResult",
    "TaskDecomposition",
    "TaskDecomposer",
    "SimpleTaskDecomposer",
    "ResultAggregator",
    "SimpleResultAggregator",
    "ModelMixer",
    # Context sharing
    "ContextManager",
    "ContextPropagator",
    "FeedbackLoop",
    "SharedContext",
    "ContextEntry",
    "context_manager",
    "context_propagator",
    "feedback_loop",
    # Intelligent caching
    "IntelligentCache",
]
