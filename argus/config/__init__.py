# argus/config/__init__.py

"""
Enhanced Configuration Management System for Gemini SRE Agent.

This module provides a comprehensive, type-safe, and environment-aware configuration
management system using Pydantic and pydantic-settings.
"""

from .app_config import AppConfig
from .base import BaseConfig, Environment
from .cli_tools import config_cli
from .dev_utils import ConfigDevUtils
from .errors import (
    ConfigEnvironmentError,
    ConfigError,
    ConfigFileError,
    ConfigSchemaError,
    ConfigValidationError,
)
from .loader import ConfigLoader
from .manager import ConfigManager
from .metrics import ConfigMetrics, ConfigMetricsCollector
from .ml_config import (
    AdaptivePromptConfig,
    CodeGenerationConfig,
    MLConfig,
    ModelConfig,
    ModelType,
)
from .monitoring import ConfigChangeEvent, ConfigMonitoring
from .secrets import SecretsConfig

__all__ = [
    "AdaptivePromptConfig",
    "AppConfig",
    # Core configuration classes
    "BaseConfig",
    "CodeGenerationConfig",
    "ConfigChangeEvent",
    "ConfigDevUtils",
    "ConfigEnvironmentError",
    # Error classes
    "ConfigError",
    "ConfigFileError",
    "ConfigLoader",
    # Management classes
    "ConfigManager",
    "ConfigMetrics",
    "ConfigMetricsCollector",
    # Monitoring and metrics
    "ConfigMonitoring",
    "ConfigSchemaError",
    "ConfigValidationError",
    "Environment",
    "MLConfig",
    "ModelConfig",
    "ModelType",
    "SecretsConfig",
    # CLI and utilities
    "config_cli",
]
