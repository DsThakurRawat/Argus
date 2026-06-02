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

# argus/source_control/provider_factory.py

import importlib
import logging

from ..config.source_control_repositories import RepositoryConfig
from .base import SourceControlProvider
from .credential_manager import CredentialManager


class ProviderFactory:
    """Creates and manages source control provider instances."""

    def __init__(self, credential_manager: CredentialManager) -> None:
        self.credential_manager = credential_manager
        self.provider_registry: dict[str, type[SourceControlProvider]] = {}
        self.logger = logging.getLogger(__name__)

    def register_provider(
        self, provider_type: str, provider_class: type[SourceControlProvider]
    ) -> None:
        """Register a provider class for a specific provider type."""
        self.provider_registry[provider_type] = provider_class
        self.logger.debug(f"Registered provider: {provider_type}")

    def register_providers_from_modules(self, module_names: list) -> None:
        """Dynamically load and register providers from specified modules."""
        for module_name in module_names:
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register_providers"):
                    module.register_providers(self)
                    self.logger.info(f"Registered providers from module: {module_name}")
            except ImportError as e:
                self.logger.error(
                    f"Failed to import provider module {module_name}: {e!s}"
                )

    async def create_provider(
        self, repo_config: RepositoryConfig
    ) -> SourceControlProvider:
        """Create a provider instance based on repository configuration."""
        provider_type = repo_config.type

        if provider_type not in self.provider_registry:
            raise ValueError(f"Unsupported provider type: {provider_type}")

        provider_class = self.provider_registry[provider_type]

        # Create and return the provider instance
        # The provider will handle credential management internally
        return provider_class(repo_config.model_dump())
