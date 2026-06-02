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


import pytest


@pytest.fixture(scope="session")
def mock_integration_config() -> None:
    """Provide mock config for integration tests when real config is unavailable"""
    return {
        "gemini_cloud_log_monitor": {
            "services": [
                {
                    "project_id": "test-project",
                    "location": "us-central1",
                    "service_name": "test-service",
                    "subscription_id": "test-subscription",
                }
            ],
            "default_model_selection": {
                "triage_model": "gemini-1.5-flash",
                "analysis_model": "gemini-1.5-pro",
                "classification_model": "gemini-2.5-flash-lite",
            },
            "default_github_config": {"repository": "test/repo", "base_branch": "main"},
        }
    }
