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

# argus/ml/specialized_generators/__init__.py

"""
Specialized code generators for different issue types.

This package contains domain-specific code generators that inherit from
BaseCodeGenerator and provide specialized patterns and validation rules
for different types of issues.
"""

from .api_generator import APICodeGenerator
from .database_generator import DatabaseCodeGenerator
from .security_generator import SecurityCodeGenerator

__all__ = [
    "APICodeGenerator",
    "DatabaseCodeGenerator",
    "SecurityCodeGenerator",
]
