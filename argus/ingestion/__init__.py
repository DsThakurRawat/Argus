# argus/ingestion/__init__.py

"""
Log Ingestion System

A pluggable architecture for ingesting logs from multiple sources with
unified processing, error handling, and monitoring capabilities.
"""

from .adapters import (
    AWSCloudWatchAdapter,
    FileSystemAdapter,
    GCPLoggingAdapter,
    GCPPubSubAdapter,
    KubernetesAdapter,
    QueuedFileSystemAdapter,
)
from .interfaces import (
    BackpressureManager,
    ConfigurationError,
    HyxResilientClient,
    LogEntry,
    LogIngestionError,
    LogIngestionInterface,
    LogParsingError,
    LogSeverity,
    LogSourceType,
    ResilienceConfig,
    SourceAlreadyRunningError,
    SourceConfig,
    SourceConnectionError,
    SourceHealth,
    SourceNotFoundError,
    SourceNotRunningError,
    create_resilience_config,
)
from .manager import LogManager
from .processor import LogProcessor
from .queues import (
    FileQueueConfig,
    FileSystemQueue,
    MemoryQueue,
    QueueConfig,
    QueueStats,
)

__all__ = [
    "AWSCloudWatchAdapter",
    "BackpressureManager",
    "ConfigurationError",
    "FileQueueConfig",
    # Adapters
    "FileSystemAdapter",
    "FileSystemQueue",
    "GCPLoggingAdapter",
    "GCPPubSubAdapter",
    # Resilience
    "HyxResilientClient",
    "KubernetesAdapter",
    "LogEntry",
    # Error handling
    "LogIngestionError",
    # Core interfaces
    "LogIngestionInterface",
    # Main components
    "LogManager",
    "LogParsingError",
    "LogProcessor",
    "LogSeverity",
    "LogSourceType",
    # Queues
    "MemoryQueue",
    "QueueConfig",
    "QueueStats",
    "QueuedFileSystemAdapter",
    "ResilienceConfig",
    "SourceAlreadyRunningError",
    "SourceConfig",
    "SourceConnectionError",
    "SourceHealth",
    "SourceNotFoundError",
    "SourceNotRunningError",
    "create_resilience_config",
]
