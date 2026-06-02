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

from unittest.mock import MagicMock

import pytest

from argus.metrics.alerting import AlertManager
from argus.metrics.metrics_manager import MetricsManager


@pytest.fixture
def mock_metrics_manager() -> None:
    """Fixture for a mocked MetricsManager."""
    mock_manager = MagicMock(spec=MetricsManager)
    mock_manager.provider_metrics = {}
    return mock_manager


def test_alert_manager_initialization() -> None:
    """
    Test Alert Manager Initialization.

    """
    config = {
        "alert_thresholds": {"health_score": 0.8},
        "notification_channels": ["slack"],
    }
    manager = AlertManager(config)
    assert manager.thresholds == {"health_score": 0.8}
    assert manager.notification_channels == ["slack"]
    assert manager.alert_history == []


def test_check_metrics_with_alerts(mock_metrics_manager: str) -> None:
    """
    Test Check Metrics With Alerts.

    Args:
        mock_metrics_manager: Description of mock_metrics_manager.

    """
    config = {"alert_thresholds": {"health_score": 0.8}}
    alert_manager = AlertManager(config)

    provider_metrics = MagicMock()
    provider_metrics.health_score = 0.7
    mock_metrics_manager.provider_metrics = {"test_provider": provider_metrics}

    alerts = alert_manager.check_metrics(mock_metrics_manager)
    assert len(alerts) == 1
    alert = alerts[0]
    assert alert.severity == "high"
    assert alert.provider_id == "test_provider"
    assert alert.metric == "health_score"
    assert alert.value == 0.7
    assert alert.threshold == 0.8


def test_check_metrics_no_alerts(mock_metrics_manager: str) -> None:
    """
    Test Check Metrics No Alerts.

    Args:
        mock_metrics_manager: Description of mock_metrics_manager.

    """
    config = {"alert_thresholds": {"health_score": 0.8}}
    alert_manager = AlertManager(config)

    provider_metrics = MagicMock()
    provider_metrics.health_score = 0.9
    mock_metrics_manager.provider_metrics = {"test_provider": provider_metrics}

    alerts = alert_manager.check_metrics(mock_metrics_manager)
    assert len(alerts) == 0
