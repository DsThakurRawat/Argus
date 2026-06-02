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

# argus/source_control/setup.py


from ..config.source_control_global import (
    SourceControlConfig,
    SourceControlGlobalConfig,
)
from .credential_manager import CredentialManager, EnvironmentBackend, FileBackend
from .provider_factory import ProviderFactory
from .providers.github.github_provider import GitHubProvider
from .providers.gitlab.gitlab_provider import GitLabProvider
from .providers.local.local_provider import LocalProvider
from .repository_manager import RepositoryManager


async def setup_repository_system(
    config: SourceControlGlobalConfig, encryption_key: str | None = None
) -> RepositoryManager:
    """Set up the complete repository management system."""

    # Set up credential manager with backends
    credential_manager = CredentialManager(encryption_key=encryption_key)
    credential_manager.register_backend("env", EnvironmentBackend(), default=True)
    credential_manager.register_backend("file", FileBackend())

    # Set up provider factory
    provider_factory = ProviderFactory(credential_manager)
    provider_factory.register_provider("github", GitHubProvider)
    provider_factory.register_provider("local", LocalProvider)
    provider_factory.register_provider("gitlab", GitLabProvider)

    # Create and initialize repository manager
    repo_manager = RepositoryManager(config, provider_factory)
    await repo_manager.initialize()

    return repo_manager


def create_default_config() -> SourceControlConfig:
    """Create a default configuration for testing purposes."""
    from ..config.source_control_repositories import (
        GitHubRepositoryConfig,
        GitLabRepositoryConfig,
        LocalRepositoryConfig,
    )

    return SourceControlConfig(
        repositories=[
            GitHubRepositoryConfig(
                name="test-github-repo", url="https://github.com/test/repo"
            ),
            LocalRepositoryConfig(name="test-local-repo", path="/tmp/test-repo"),
            GitLabRepositoryConfig(
                name="test-gitlab-repo",
                project_id="123456",
                url="https://gitlab.com/test/repo",
            ),
        ]
    )
