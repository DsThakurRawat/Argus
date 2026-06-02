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
    # Resilience patterns
    "BackpressureManager",
    "HyxResilientClient",
    "create_resilience_config",
    "ResilienceConfig",
]
