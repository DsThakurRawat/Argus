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

# argus/pattern_detector/__init__.py

"""
Pattern Detection System
"""

from .baseline_tracker import BaselineTracker
from .confidence_scorer import ConfidenceScorer
from .models import (
    ConfidenceFactors,
    ConfidenceRule,
    ConfidenceScore,
    LogEntry,
    PatternMatch,
    PatternType,
    ThresholdConfig,
    ThresholdResult,
    ThresholdType,
    TimeWindow,
)
from .pattern_classifier import PatternClassifier
from .threshold_evaluator import ThresholdEvaluator
from .time_window_accumulator import LogAccumulator, WindowManager

__all__ = [
    "BaselineTracker",
    "ConfidenceFactors",
    "ConfidenceRule",
    "ConfidenceScore",
    "ConfidenceScorer",
    "LogAccumulator",
    "LogEntry",
    "PatternClassifier",
    "PatternMatch",
    "PatternType",
    "ThresholdConfig",
    "ThresholdEvaluator",
    "ThresholdResult",
    "ThresholdType",
    "TimeWindow",
    "WindowManager",
]
