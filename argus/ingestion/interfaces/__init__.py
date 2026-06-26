# argus/ingestion/interfaces/__init__.py

"""
Core interfaces for the log ingestion system.
"""

from .core import (
    LogEntry,
    LogIngestionInterface,
    LogSeverity,
    LogSourceType,
    SourceConfig,
    SourceHealth,
)
from .errors import (
    ConfigurationError,
    LogIngestionError,
    LogParsingError,
    SourceAlreadyRunningError,
    SourceConnectionError,
    SourceNotFoundError,
    SourceNotRunningError,
)
from .resilience import (
    BackpressureManager,
    HyxResilientClient,
    ResilienceConfig,
    create_resilience_config,
)

__all__ = [
    # Resilience patterns
    "BackpressureManager",
    "ConfigurationError",
    "HyxResilientClient",
    "LogEntry",
    # Error handling
    "LogIngestionError",
    # Core interfaces
    "LogIngestionInterface",
    "LogParsingError",
    "LogSeverity",
    "LogSourceType",
    "ResilienceConfig",
    "SourceAlreadyRunningError",
    "SourceConfig",
    "SourceConnectionError",
    "SourceHealth",
    "SourceNotFoundError",
    "SourceNotRunningError",
    "create_resilience_config",
]
