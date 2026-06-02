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

# argus/llm/provider_framework/examples/simple_provider.py

"""
Example: Simple Provider Implementation

This example shows how to create a new provider with minimal code using the framework.
This provider can be implemented in less than 50 lines of code.
"""


from ...base import ModelType
from ...config import LLMProviderConfig
from ..templates import HTTPAPITemplate


class SimpleProvider(HTTPAPITemplate):
    """
    Simple provider implementation using the HTTP API template.

    This provider demonstrates how to create a new provider with minimal code
    by leveraging the framework's templates and base classes.
    """

    def _get_default_base_url(self) -> str:
        """Override to set the default base URL for this provider."""
        return "https://api.simple-llm.com/v1"

    def _get_model_mapping(self) -> dict[ModelType, str]:
        """Define the model mapping for this provider."""
        return {
            ModelType.FAST: "simple-fast",
            ModelType.SMART: "simple-smart",
        }

    def _get_headers(self) -> dict[str, str]:
        """Override to use custom headers for this provider."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Provider": "simple-llm",
        }

    @classmethod
    def validate_config(cls, config: LLMProviderConfig) -> None:
        """Validate provider-specific configuration."""
        super().validate_config(config)

        # Add custom validation for this provider
        if not config.api_key or len(config.api_key) < 10:
            raise ValueError(
                "Simple provider requires a valid API key of at least 10 characters"
            )


# That's it! This provider is now ready to use.
# The framework handles all the common functionality like:
# - HTTP requests and error handling
# - Circuit breaker pattern
# - Health checks
# - Model selection
# - Response parsing
