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
    from argus.core.logging import get_logger, FlowTracker

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
    "Alert",
    "AlertManager",
    "AlertRule",
    "AlertSeverity",
    "AlertStatus",
    # New comprehensive logging components
    "ComprehensiveLogger",
    "ConfigurationError",
    # Handlers
    "ConsoleHandler",
    "FileHandler",
    "FlowContext",
    "FlowFormatter",
    # Flow Tracking
    "FlowTracker",
    "FlowTrackingError",
    # Formatters
    "JSONFormatter",
    "LogFormat",
    "LogLevel",
    # Configuration
    "LoggingConfig",
    "LoggingConfigManager",
    "LoggingContext",
    # Exceptions
    "LoggingError",
    # Manager
    "LoggingManager",
    # Metrics
    "LoggingMetrics",
    "MetricsCollector",
    "MetricsError",
    "PerformanceMonitor",
    "RemoteHandler",
    "RotatingFileHandler",
    "StructuredFormatter",
    # Structured Logging
    "StructuredLogger",
    "SyslogHandler",
    "TextFormatter",
    "configure_logging",
    "get_alert_manager",
    "get_logger",
    "get_performance_monitor",
]
