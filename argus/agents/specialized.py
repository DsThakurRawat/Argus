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

# argus/agents/specialized.py

"""
Specialized agent classes for different types of tasks.

This module provides specialized agent classes that inherit from BaseAgent
and are tailored for specific types of tasks like text generation, analysis,
and code generation.
"""


from ..llm.service import LLMService
from .base import BaseAgent
from .response_models import AnalysisResponse, CodeResponse, TextResponse


class TextAgent(BaseAgent[TextResponse]):
    """Agent specialized for text generation tasks."""

    def __init__(
        self,
        llm_service: LLMService,
        primary_model: str = "smart",
        fallback_model: str | None = "fast",
    ):
        super().__init__(
            llm_service=llm_service,
            response_model=TextResponse,
            primary_model=primary_model,
            fallback_model=fallback_model,
        )

    async def generate_text(self, prompt: str, **kwargs) -> TextResponse:
        """Generate text using the agent."""
        return await self.execute(
            prompt_name="generate_text", prompt_args={"input": prompt, **kwargs}
        )


class AnalysisAgent(BaseAgent[AnalysisResponse]):
    """Agent specialized for analysis tasks."""

    def __init__(
        self,
        llm_service: LLMService,
        primary_model: str = "smart",
        fallback_model: str | None = None,  # No fallback by default for analysis
    ):
        super().__init__(
            llm_service=llm_service,
            response_model=AnalysisResponse,
            primary_model=primary_model,
            fallback_model=fallback_model,
        )

    async def analyze(
        self, content: str, criteria: list[str], **kwargs
    ) -> AnalysisResponse:
        """Analyze content based on provided criteria."""
        return await self.execute(
            prompt_name="analyze_content",
            prompt_args={"content": content, "criteria": criteria, **kwargs},
        )


class CodeAgent(BaseAgent[CodeResponse]):
    """Agent specialized for code generation tasks."""

    def __init__(
        self,
        llm_service: LLMService,
        primary_model: str = "code",
        fallback_model: str | None = "smart",
    ):
        super().__init__(
            llm_service=llm_service,
            response_model=CodeResponse,
            primary_model=primary_model,
            fallback_model=fallback_model,
        )

    async def generate_code(
        self, description: str, language: str, **kwargs
    ) -> CodeResponse:
        """Generate code based on description and language."""
        return await self.execute(
            prompt_name="generate_code",
            prompt_args={"description": description, "language": language, **kwargs},
        )
