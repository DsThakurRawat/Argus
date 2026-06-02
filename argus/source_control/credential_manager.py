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

# argus/source_control/credential_manager.py

"""
Credential manager module.

This module provides backward compatibility imports for the refactored credential management system.
"""

# Import all classes from the new credential_management package
from .credential_management import (
    AWSSecretsBackend,
    AzureKeyVaultBackend,
    CredentialBackend,
    CredentialManager,
    CredentialRotationManager,
    EnvironmentBackend,
    FileBackend,
    VaultBackend,
)

# Re-export all classes for backward compatibility
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
