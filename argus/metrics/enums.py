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

# argus/metrics/enums.py

from enum import Enum


class ErrorCategory(Enum):
    """
    Categories for errors that occur during LLM requests.
    """

    TRANSIENT = "transient"
    """Transient errors that may be resolved by retrying."""

    AUTHENTICATION = "authentication"
    """Errors related to authentication or authorization."""

    NOT_FOUND = "not_found"
    """Errors indicating that the requested resource was not found."""

    RATE_LIMIT = "rate_limit"
    """Errors due to exceeding rate limits."""

    BAD_REQUEST = "bad_request"
    """Errors caused by invalid or malformed requests."""

    SERVER_ERROR = "server_error"
    """Errors originating from the server."""

    TIMEOUT = "timeout"
    """Errors due to request timeouts."""

    UNKNOWN = "unknown"
    """Errors of unknown or uncategorized type."""
