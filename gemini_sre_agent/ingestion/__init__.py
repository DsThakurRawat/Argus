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

# gemini_sre_agent/ingestion/__init__.py

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
    # Core interfaces
    "LogIngestionInterface",
    "LogEntry",
    "LogSeverity",
    "SourceHealth",
    "SourceConfig",
    "LogSourceType",
    # Error handling
    "LogIngestionError",
    "SourceConnectionError",
    "LogParsingError",
    "ConfigurationError",
    "SourceNotFoundError",
    "SourceAlreadyRunningError",
    "SourceNotRunningError",
    "BackpressureManager",
    # Resilience
    "HyxResilientClient",
    "create_resilience_config",
    "ResilienceConfig",
    # Adapters
    "FileSystemAdapter",
    "QueuedFileSystemAdapter",
    "GCPLoggingAdapter",
    "GCPPubSubAdapter",
    "AWSCloudWatchAdapter",
    "KubernetesAdapter",
    # Queues
    "MemoryQueue",
    "QueueConfig",
    "QueueStats",
    "FileSystemQueue",
    "FileQueueConfig",
    # Main components
    "LogManager",
    "LogProcessor",
]
