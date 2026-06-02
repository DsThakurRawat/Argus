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

# gemini_sre_agent/source_control/credential_management/backends.py

"""
Credential storage backends module.

This module contains all credential storage backend implementations.
"""

from abc import ABC, abstractmethod
import os


class CredentialBackend(ABC):
    """Abstract base class for credential storage backends."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Retrieve a credential value by key."""
        pass

    @abstractmethod
    async def set(self, key: str, value: str) -> None:
        """Store a credential value by key."""
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Delete a credential by key."""
        pass


class EnvironmentBackend(CredentialBackend):
    """Credential backend using environment variables."""

    async def get(self, key: str) -> str | None:
        return os.environ.get(key)

    async def set(self, key: str, value: str) -> None:
        os.environ[key] = value

    async def delete(self, key: str) -> None:
        if key in os.environ:
            del os.environ[key]


class FileBackend(CredentialBackend):
    """Credential backend using file storage."""

    def __init__(self, base_path: str = "/tmp/credentials") -> None:
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def _get_file_path(self, key: str) -> str:
        """Get the file path for a given key."""
        # Sanitize the key to prevent directory traversal
        safe_key = "".join(c for c in key if c.isalnum() or c in "._-")
        return os.path.join(self.base_path, f"{safe_key}.json")

    async def get(self, key: str) -> str | None:
        file_path = self._get_file_path(key)
        if not os.path.exists(file_path):
            return None

        try:
            with open(file_path) as f:
                return f.read()
        except OSError:
            return None

    async def set(self, key: str, value: str) -> None:
        file_path = self._get_file_path(key)
        try:
            with open(file_path, "w") as f:
                f.write(value)
        except OSError as e:
            raise RuntimeError(
                f"Failed to write credential file {file_path}: {e}"
            ) from e

    async def delete(self, key: str) -> None:
        file_path = self._get_file_path(key)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except OSError:
                pass
