# argus/agents/agent_models.py

"""
Main coordination module for agent models.

This module serves as the main coordination point for all agent-related models,
importing and re-exporting models from specialized modules while maintaining
backward compatibility. It provides a clean, organized interface to all agent
models including request models, response models, state models, and validation utilities.

The module is organized as follows:
- Common enums and base models are defined here
- Specialized models are imported from dedicated modules
- All exports are maintained for backward compatibility
- Module-level utilities and factory functions are provided
"""

from enum import Enum
from typing import Any

# Import from request_models (when created)
# from .request_models import *
# Import from response_models
# Base models; Response models; Supporting models; Factory functions; Registry and utilities
from .response_models import (
    AGENT_RESPONSE_MODELS,
    AnalysisFinding,
    AnalysisResult,
    BaseAgentResponse,
    CodeResponse,
    ComponentHealth,
    HealthCheckResponse,
    RemediationPlan,
    RemediationStep,
    ResourceUtilization,
    RootCauseAnalysis,
    StatusCode,
    TextResponse,
    TriageResult,
    ValidationError,
    create_analysis_result,
    create_health_check_response,
    create_remediation_plan,
    create_triage_result,
    get_response_model,
    validate_response_model,
)

# Import from state_models
from .state_models import (
    AgentExecutionContext,
    AgentExecutionMetrics,
    AgentExecutionState,
    AgentState,
    ConversationHistory,
    PersistentAgentData,
    StateManager,
    StateSnapshot,
    StateTransitionEnum,  # State enums
    WorkflowContext,
    WorkflowState,
    WorkflowStep,
)

# Import from validation_models
# Validation error models; Validation schemas; Validation utilities;
# Custom validators; Validation decorators
from .validation_models import (
    CodeAnalysisValidationSchema,
    LogValidationSchema,
    MetricValidationSchema,
    ValidationRegistry,
    ValidationResult,
    ValidationSeverity,
    ValidationUtils,
    ValidationWarning,
    validate_confidence,
    validate_confidence_score,
    validate_confidence_threshold,
    validate_enum_value,
    validate_non_empty_string,
    validate_positive_number,
    validate_severity,
    validate_severity_level,
    validate_timestamp,
    validate_uuid_format,
    validate_with_schema,
)

# ============================================================================
# Common Enums and Base Models
# ============================================================================


class SeverityLevel(str, Enum):
    """Severity levels for issues and alerts."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class ConfidenceLevel(str, Enum):
    """Confidence levels for agent assessments."""

    VERY_HIGH = "very_high"  # 0.9-1.0
    HIGH = "high"  # 0.7-0.9
    MEDIUM = "medium"  # 0.5-0.7
    LOW = "low"  # 0.3-0.5
    VERY_LOW = "very_low"  # 0.0-0.3


class IssueCategory(str, Enum):
    """Categories for different types of issues."""

    PERFORMANCE = "performance"
    SECURITY = "security"
    RELIABILITY = "reliability"
    USABILITY = "usability"
    COMPATIBILITY = "compatibility"
    DATA_QUALITY = "data_quality"
    INFRASTRUCTURE = "infrastructure"
    CODE_QUALITY = "code_quality"
    DEPLOYMENT = "deployment"
    MONITORING = "monitoring"


class ActionType(str, Enum):
    """Types of actions that can be recommended."""

    IMMEDIATE = "immediate"
    SHORT_TERM = "short_term"
    LONG_TERM = "long_term"
    INVESTIGATION = "investigation"
    MONITORING = "monitoring"


# ============================================================================
# Module-level Utilities
# ============================================================================


def get_all_response_models() -> dict[str, type]:
    """Get all available response models."""
    return AGENT_RESPONSE_MODELS.copy()


def get_all_state_models() -> dict[str, type]:
    """Get all available state models."""
    return {
        "AgentExecutionState": AgentExecutionState,
        "WorkflowContext": WorkflowContext,
        "ConversationHistory": ConversationHistory,
        "PersistentAgentData": PersistentAgentData,
    }


def get_all_validation_models() -> dict[str, type]:
    """Get all available validation models."""
    return {
        "ValidationError": ValidationError,
        "ValidationWarning": ValidationWarning,
        "ValidationResult": ValidationResult,
        "MetricValidationSchema": MetricValidationSchema,
        "LogValidationSchema": LogValidationSchema,
        "CodeAnalysisValidationSchema": CodeAnalysisValidationSchema,
    }


def create_agent_response(
    agent_type: str, agent_id: str, status: StatusCode = StatusCode.SUCCESS, **kwargs
) -> BaseAgentResponse:
    """Create an agent response using the appropriate model."""
    model_class = get_response_model(agent_type)
    return model_class(agent_type=agent_type, agent_id=agent_id, status=status, **kwargs)


def validate_agent_data(
    data: dict[str, Any], data_type: str = "agent_response"
) -> ValidationResult:
    """Validate agent data using the appropriate validator."""
    if data_type == "agent_response":
        return ValidationUtils.validate_agent_response_data(data)
    elif data_type == "workflow":
        return ValidationUtils.validate_workflow_data(data)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


# ============================================================================
# Module Exports
# ============================================================================

__all__ = [
    # Registry and utilities
    "AGENT_RESPONSE_MODELS",
    "ActionType",
    "AgentExecutionContext",
    "AgentExecutionMetrics",
    "AgentExecutionState",
    # State models
    "AgentState",
    # Supporting response models
    "AnalysisFinding",
    "AnalysisResult",
    # Base models
    "BaseAgentResponse",
    "CodeAnalysisValidationSchema",
    "CodeResponse",
    "ComponentHealth",
    "ConfidenceLevel",
    "ConversationHistory",
    "HealthCheckResponse",
    "IssueCategory",
    "LogValidationSchema",
    "MetricValidationSchema",
    "PersistentAgentData",
    "RemediationPlan",
    "RemediationStep",
    "ResourceUtilization",
    "RootCauseAnalysis",
    "SeverityLevel",
    # State utilities
    "StateManager",
    "StateSnapshot",
    "StateTransitionEnum",
    # Common enums
    "StatusCode",
    "TextResponse",
    # Response models
    "TriageResult",
    "ValidationError",
    "ValidationRegistry",
    "ValidationResult",
    "ValidationSeverity",
    # Validation utilities
    "ValidationUtils",
    # Validation models
    "ValidationWarning",
    "WorkflowContext",
    "WorkflowState",
    "WorkflowStep",
    "create_agent_response",
    "create_analysis_result",
    "create_health_check_response",
    "create_remediation_plan",
    # Factory functions
    "create_triage_result",
    "get_all_response_models",
    "get_all_state_models",
    "get_all_validation_models",
    "get_response_model",
    "validate_agent_data",
    "validate_confidence",
    "validate_confidence_score",
    "validate_confidence_threshold",
    "validate_enum_value",
    "validate_non_empty_string",
    "validate_positive_number",
    "validate_response_model",
    "validate_severity",
    "validate_severity_level",
    "validate_timestamp",
    "validate_uuid_format",
    "validate_with_schema",
]


# All old model definitions have been moved to specialized modules
# This file now serves as a coordination module that imports and re-exports
# all models while maintaining backward compatibility
