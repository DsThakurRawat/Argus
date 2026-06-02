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

# argus/source_control/providers/__init__.py

"""
Source control provider implementations.

This package contains concrete implementations of the SourceControlProvider
interface for different source control systems like GitHub, GitLab, and local repositories.
"""

from .github.github_provider import GitHubProvider
from .gitlab.gitlab_provider import GitLabProvider
from .local.local_provider import LocalProvider

__all__ = [
    "GitHubProvider",
    "GitLabProvider",
    "LocalProvider",
]
