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

"""Standardized logging system for the Gemini SRE Agent.

This module provides a comprehensive logging framework that supports:
- Structured logging with consistent formats
- Flow tracking with unique identifiers
- Contextual information and metadata
- Performance monitoring and metrics
- Environment-specific configurations
- Integration with monitoring systems
- Thread-safe operations
- Configurable log levels and outputs

The main components are:
- LoggingManager: Central logging orchestrator
- StructuredLogger: Enhanced logger with structured output
- FlowTracker: Tracks operations across the system
- LogFormatter: Custom formatters for different output types
- LogHandler: Handlers for various output destinations
- MetricsCollector: Collects and reports logging metrics

Example usage:
    from gemini_sre_agent.core.logging import get_logger, FlowTracker

    # Get a logger
    logger = get_logger(__name__)

    # Track a flow
    with FlowTracker("operation_name") as flow:
        logger.info("Starting operation", extra={"flow_id": flow.flow_id})
        # ... do work ...
        logger.info("Operation completed", extra={"flow_id": flow.flow_id})
"""

from .alerting import (
    Alert,
    AlertManager,
    AlertRule,
    AlertSeverity,
    AlertStatus,
    get_alert_manager,
)
from .config import LoggingConfig, LoggingConfigManager
from .context import LoggingContext
from .exceptions import (
    ConfigurationError,
    FlowTrackingError,
    LoggingError,
    MetricsError,
)
from .flow_tracker import FlowContext, FlowTracker
from .formatters import FlowFormatter, JSONFormatter, StructuredFormatter, TextFormatter
from .handlers import (
    ConsoleHandler,
)
from .handlers import (
    DatabaseHandler as SyslogHandler,
)
from .handlers import (
    HTTPHandler as RemoteHandler,
)
from .handlers import (
    RotatingStructuredFileHandler as RotatingFileHandler,
)
from .handlers import (
    StructuredFileHandler as FileHandler,
)

# New comprehensive logging components
from .logger import Logger as ComprehensiveLogger
from .manager import LoggingManager, configure_logging, get_logger
from .metrics import LoggingMetrics, MetricsCollector
from .performance_monitor import PerformanceMonitor, get_performance_monitor
from .structured import LogFormat, LogLevel, StructuredLogger

__all__ = [
    # Manager
    "LoggingManager",
    "get_logger",
    "configure_logging",
    # Structured Logging
    "StructuredLogger",
    "LogLevel",
    "LogFormat",
    # Flow Tracking
    "FlowTracker",
    "FlowContext",
    # Formatters
    "JSONFormatter",
    "TextFormatter",
    "StructuredFormatter",
    "FlowFormatter",
    # Handlers
    "ConsoleHandler",
    "FileHandler",
    "RotatingFileHandler",
    "SyslogHandler",
    "RemoteHandler",
    # Metrics
    "LoggingMetrics",
    "MetricsCollector",
    # Configuration
    "LoggingConfig",
    "LoggingConfigManager",
    # Exceptions
    "LoggingError",
    "ConfigurationError",
    "FlowTrackingError",
    "MetricsError",
    # New comprehensive logging components
    "ComprehensiveLogger",
    "PerformanceMonitor",
    "get_performance_monitor",
    "AlertManager",
    "AlertRule",
    "Alert",
    "AlertSeverity",
    "AlertStatus",
    "get_alert_manager",
    "LoggingContext",
]
