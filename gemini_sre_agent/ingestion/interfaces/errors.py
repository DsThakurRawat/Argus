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

# gemini_sre_agent/ingestion/interfaces/errors.py

"""
Error handling classes for log ingestion system.
"""


class LogIngestionError(Exception):
    """Base exception for ingestion errors."""

    pass


class SourceConnectionError(LogIngestionError):
    """Connection to source failed."""

    pass


class LogParsingError(LogIngestionError):
    """Failed to parse log entry."""

    pass


class ConfigurationError(LogIngestionError):
    """Configuration validation or loading error."""

    pass


class SourceNotFoundError(LogIngestionError):
    """Requested log source not found."""

    pass


class SourceAlreadyRunningError(LogIngestionError):
    """Attempt to start an already running source."""

    pass


class SourceNotRunningError(LogIngestionError):
    """Attempt to stop a source that is not running."""

    pass
