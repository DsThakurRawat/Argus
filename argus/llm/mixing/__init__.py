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
    "ContextEntry",
    # Context sharing
    "ContextManager",
    "ContextPropagator",
    "FeedbackLoop",
    # Intelligent caching
    "IntelligentCache",
    "MixingResult",
    # Model mixing
    "MixingStrategy",
    "ModelConfig",
    "ModelMixer",
    "ResultAggregator",
    "SharedContext",
    "SimpleResultAggregator",
    "SimpleTaskDecomposer",
    "TaskDecomposer",
    "TaskDecomposition",
    "TaskType",
    "context_manager",
    "context_propagator",
    "feedback_loop",
]
