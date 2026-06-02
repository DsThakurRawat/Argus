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

from unittest.mock import MagicMock, patch

import pytest

from argus.log_ingestion import LogIngestor


@pytest.fixture
def mock_logging_client() -> None:
    """
    Mock Logging Client.

    """
    with patch("argus.log_ingestion.LoggingServiceV2Client") as mock_client:
        yield mock_client


def test_get_logs(mock_logging_client: str) -> None:
    """
    Test Get Logs.

    Args:
        mock_logging_client: Description of mock_logging_client.

    """
    # Arrange
    mock_client_instance = mock_logging_client.return_value
    mock_client_instance.list_log_entries.return_value = [
        MagicMock(payload="log entry 1"),
        MagicMock(payload="log entry 2"),
    ]
    ingestor = LogIngestor(project_id="test-project")

    # Act
    logs = ingestor.get_logs(filter_str="severity>=ERROR", limit=2)

    # Assert
    assert logs == ["log entry 1", "log entry 2"]
    mock_client_instance.list_log_entries.assert_called_once_with(
        request={
            "resource_names": ["projects/test-project"],
            "filter": "severity>=ERROR",
            "page_size": 2,
        }
    )
