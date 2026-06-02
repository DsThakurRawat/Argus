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

# gemini_sre_agent/config/__init__.py

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
    # Core configuration classes
    "BaseConfig",
    "Environment",
    "AppConfig",
    "MLConfig",
    "ModelConfig",
    "ModelType",
    "CodeGenerationConfig",
    "AdaptivePromptConfig",
    "SecretsConfig",
    # Error classes
    "ConfigError",
    "ConfigValidationError",
    "ConfigFileError",
    "ConfigEnvironmentError",
    "ConfigSchemaError",
    # Management classes
    "ConfigManager",
    "ConfigLoader",
    # CLI and utilities
    "config_cli",
    "ConfigDevUtils",
    # Monitoring and metrics
    "ConfigMonitoring",
    "ConfigChangeEvent",
    "ConfigMetricsCollector",
    "ConfigMetrics",
]
