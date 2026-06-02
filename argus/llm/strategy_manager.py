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

# argus/llm/strategy_manager.py

"""
Strategy manager for model selection using the Strategy pattern.

This module provides a comprehensive strategy management system for selecting
the most appropriate LLM model based on different optimization goals such as
cost, performance, quality, and time-based considerations.

The Strategy pattern is implemented with:
- Abstract base class for strategies
- Concrete strategy implementations
- Strategy manager for selection and management
- Performance tracking and metrics

This module now serves as a coordination layer that imports and re-exports
functionality from the specialized strategy modules:
- strategy_base.py: Base classes and common types
- strategy_implementations.py: Concrete strategy implementations
- strategy_selector.py: Strategy manager and selection logic
- strategy_metrics.py: Performance metrics and monitoring

Classes:
    StrategyManager: Main manager for model selection strategies
    OptimizationGoal: Enum for different optimization goals
    StrategyContext: Context data for strategy execution
    StrategyResult: Result data from strategy execution
    ScoringWeights: Configuration for model scoring weights
    ScoringContext: Context for model scoring operations
    ModelScore: Score data for model evaluation
    ModelSelectionStrategy: Abstract base class for strategies
    CostOptimizedStrategy: Strategy that prioritizes cost efficiency
    PerformanceOptimizedStrategy: Strategy that prioritizes performance
    QualityOptimizedStrategy: Strategy that prioritizes quality
    TimeBasedStrategy: Strategy that adapts based on time of day
    HybridStrategy: Strategy that balances multiple factors with learning
    StrategyMetricsCollector: Collects and analyzes strategy performance metrics
    StrategyPerformanceAnalyzer: Analyzes strategy performance patterns
    StrategyRecommendationEngine: Provides strategy recommendations based on metrics

Author: Gemini SRE Agent
Created: 2024
"""

# Import all strategy functionality from specialized modules
from .strategy_base import (
    ModelScore,
    ModelSelectionStrategy,
    OptimizationGoal,
    StrategyContext,
    ScoringWeights,
    StrategyResult,
)
from .strategy_implementations import (
    CostOptimizedStrategy,
    HybridStrategy,
    PerformanceOptimizedStrategy,
    QualityOptimizedStrategy,
    TimeBasedStrategy,
)
from .strategy_metrics import (
    PerformanceSnapshot,
    StrategyMetrics,
    StrategyMetricsCollector,
    StrategyPerformanceAnalyzer,
    StrategyRecommendationEngine,
)
from .strategy_selector import StrategyManager

# Re-export everything for backward compatibility
__all__ = [
    # Base classes and types
    "OptimizationGoal",
    "StrategyContext",
    "StrategyResult",
    "ScoringWeights",
    "ModelScore",
    "ModelSelectionStrategy",
    # Strategy implementations
    "CostOptimizedStrategy",
    "PerformanceOptimizedStrategy",
    "QualityOptimizedStrategy",
    "TimeBasedStrategy",
    "HybridStrategy",
    # Main manager
    "StrategyManager",
    # Metrics and monitoring
    "StrategyMetrics",
    "PerformanceSnapshot",
    "StrategyMetricsCollector",
    "StrategyPerformanceAnalyzer",
    "StrategyRecommendationEngine",
]

# For backward compatibility, create a default strategy manager instance

_default_manager: StrategyManager | None = None


def get_default_strategy_manager() -> StrategyManager:
    """Get the default strategy manager instance.

    Returns:
        Default StrategyManager instance
    """
    global _default_manager
    if _default_manager is None:
        _default_manager = StrategyManager()
    return _default_manager


def reset_default_strategy_manager() -> None:
    """Reset the default strategy manager instance."""
    global _default_manager
    _default_manager = None
