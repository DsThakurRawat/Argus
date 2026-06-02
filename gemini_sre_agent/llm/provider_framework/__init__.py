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

# gemini_sre_agent/llm/provider_framework/__init__.py

"""
Provider Addition Framework for Multi-LLM Provider Support.

This package provides a comprehensive framework for easily adding new LLM providers
with minimal code, automatic registration, validation, and plugin support.
"""

from .auto_registry import ProviderAutoRegistry
from .base_template import BaseProviderTemplate
from .capability_discovery import ProviderCapabilityDiscovery
from .plugin_loader import ProviderPluginLoader
from .templates import (
    HTTPAPITemplate,
    OpenAICompatibleTemplate,
    RESTAPITemplate,
    StreamingTemplate,
)
from .validator import ProviderValidator

__all__ = [
    "BaseProviderTemplate",
    "HTTPAPITemplate",
    "OpenAICompatibleTemplate",
    "ProviderAutoRegistry",
    "ProviderCapabilityDiscovery",
    "ProviderPluginLoader",
    "ProviderValidator",
    "RESTAPITemplate",
    "StreamingTemplate",
]
