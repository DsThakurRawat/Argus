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

# argus/llm/capabilities/database.py

import logging

from argus.llm.capabilities.models import ModelCapabilities

logger = logging.getLogger(__name__)


class CapabilityDatabase:
    """
    A database for storing and querying model capabilities.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, ModelCapabilities] = {}

    def add_capabilities(self, model_capabilities: ModelCapabilities) -> None:
        """
        Add or update capabilities for a model.

        Args:
            model_capabilities: The ModelCapabilities object to add.
        """
        self._capabilities[model_capabilities.model_id] = model_capabilities
        logger.info(
            f"Added/updated capabilities for model: {model_capabilities.model_id}"
        )

    def get_capabilities(self, model_id: str) -> ModelCapabilities | None:
        """
        Retrieve capabilities for a specific model.

        Args:
            model_id: The unique identifier for the model.

        Returns:
            ModelCapabilities object if found, None otherwise.
        """
        return self._capabilities.get(model_id)

    def query_capabilities(
        self, capability_name: str | None = None
    ) -> list[ModelCapabilities]:
        """
        Query models based on their capabilities.

        Args:
            capability_name: Optional. The name of the capability to query for.

        Returns:
            A list of ModelCapabilities objects that match the query.
        """
        results = []
        for model_caps in self._capabilities.values():
            if capability_name:
                if any(cap.name == capability_name for cap in model_caps.capabilities):
                    results.append(model_caps)
            else:
                results.append(model_caps)
        return results

    def clear(self) -> None:
        """
        Clear all capabilities from the database.
        """
        self._capabilities.clear()
        logger.info("Capability database cleared.")

    def __len__(self) -> int:
        return len(self._capabilities)

    def __contains__(self, model_id: str) -> bool:
        return model_id in self._capabilities

    def get_all_model_ids(self) -> list[str]:
        """
        Get all model IDs in the database.

        Returns:
            A list of all model IDs.
        """
        return list(self._capabilities.keys())
