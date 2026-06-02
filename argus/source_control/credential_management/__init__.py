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

# argus/source_control/credential_management/__init__.py

"""
Credential management package.

This package provides secure credential storage, retrieval, and rotation capabilities.
"""

from .backends import (
    CredentialBackend,
    EnvironmentBackend,
    FileBackend,
)
from .cloud_backends import (
    AWSSecretsBackend,
    AzureKeyVaultBackend,
    VaultBackend,
)
from .manager import CredentialManager
from .rotation import CredentialRotationManager

__all__ = [
    "AWSSecretsBackend",
    "AzureKeyVaultBackend",
    "CredentialBackend",
    "CredentialManager",
    "CredentialRotationManager",
    "EnvironmentBackend",
    "FileBackend",
    "VaultBackend",
]
