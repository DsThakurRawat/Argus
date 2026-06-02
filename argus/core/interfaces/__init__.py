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

# argus/core/interfaces/__init__.py

"""
Core interfaces for the Gemini SRE Agent system.

This package provides abstract base classes and interfaces that form
the foundation for all major components in the system.
"""

from .agent import (
    AgentCoordinator,
    AnalysisAgent,
    BaseAgent,
    RemediationAgent,
    TriageAgent,
)
from .base import (
    BaseComponent,
    ConfigurableComponent,
    MonitorableComponent,
    ProcessableComponent,
    StatefulComponent,
)
from .llm import (
    ChatModel,
    CompletionModel,
    EmbeddingModel,
    LLMManager,
    LLMModel,
    LLMProvider,
)
from .protocols import (  # Additional protocols
    AgentLike,
    Aggregator,
    Alertable,
    AsyncBatchProcessor,
    AsyncProcessable,
    BatchProcessor,
    Cacheable,
    CircuitBreaker,
    Configurable,
    CostTrackable,
    Deserializable,
    EventEmitter,
    EventListener,
    FallbackProvider,
    Filter,
    HealthCheckable,
    Identifiable,
    LoadBalancer,
    LockManager,
    Loggable,
    MetricsCollector,
    ModelLike,
    Observer,
    Pipeline,
    Processable,
    ProviderLike,
    RateLimited,
    RequestLike,
    ResourceManager,
    ResponseLike,
    Retryable,
    Scheduler,
    Serializable,
    Stateful,
    Streamable,
    Subject,
    Timestamped,
    TokenCountable,
    Transformer,
    Validatable,
    WorkflowOrchestrator,
    WorkflowStep,
    get_protocol_methods,
    implements_protocol,
    validate_protocol_implementation,
)

__all__ = [
    # Base interfaces
    "BaseComponent",
    "ConfigurableComponent",
    "StatefulComponent",
    "ProcessableComponent",
    "MonitorableComponent",
    # Agent interfaces
    "BaseAgent",
    "TriageAgent",
    "AnalysisAgent",
    "RemediationAgent",
    "AgentCoordinator",
    # LLM interfaces
    "LLMProvider",
    "LLMModel",
    "ChatModel",
    "CompletionModel",
    "EmbeddingModel",
    "LLMManager",
    # Protocol classes
    "Serializable",
    "Deserializable",
    "Identifiable",
    "Timestamped",
    "Configurable",
    "Stateful",
    "Loggable",
    "Validatable",
    "HealthCheckable",
    "MetricsCollector",
    "Alertable",
    "Processable",
    "AsyncProcessable",
    "Streamable",
    "Cacheable",
    "Retryable",
    "RateLimited",
    "CostTrackable",
    "TokenCountable",
    "AgentLike",
    "ProviderLike",
    "ModelLike",
    "RequestLike",
    "ResponseLike",
    "WorkflowStep",
    "WorkflowOrchestrator",
    "EventEmitter",
    "EventListener",
    "ResourceManager",
    "LoadBalancer",
    "CircuitBreaker",
    "FallbackProvider",
    "BatchProcessor",
    "AsyncBatchProcessor",
    "Pipeline",
    "Transformer",
    "Filter",
    "Aggregator",
    "Scheduler",
    "LockManager",
    "Observer",
    "Subject",
    # Protocol utilities
    "implements_protocol",
    "get_protocol_methods",
    "validate_protocol_implementation",
]
