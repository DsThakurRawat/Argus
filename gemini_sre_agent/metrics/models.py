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

# gemini_sre_agent/metrics/models.py

from typing import Literal

from pydantic import BaseModel, Field


class Alert(BaseModel):
    """A class to represent an alert."""

    severity: Literal["high", "medium", "low"] = Field(
        ..., description="The severity of the alert."
    )
    provider_id: str = Field(
        ..., description="The ID of the provider that triggered the alert."
    )
    message: str = Field(..., description="A human-readable message for the alert.")
    metric: str = Field(..., description="The metric that triggered the alert.")
    value: float = Field(
        ..., description="The value of the metric that triggered the alert."
    )
    threshold: float = Field(..., description="The threshold for the metric.")
