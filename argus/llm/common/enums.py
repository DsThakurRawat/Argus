#

# argus/llm/common/enums.py

from enum import Enum


class ProviderType(str, Enum):
    """Supported LLM provider types."""

    GEMINI = "gemini"
    OLLAMA = "ollama"
    CLAUDE = "claude"
    OPENAI = "openai"
    GROK = "grok"
    BEDROCK = "bedrock"
    GROQ = "groq"
    AZURE = "azure"
    MISTRAL = "mistral"
    XAI = "xai"
    PERPLEXITY = "perplexity"
    OPENROUTER = "openrouter"
    ANTHROPIC = "anthropic"
    TEST = "test"
    TEST_PROVIDER = "test_provider"


class ModelType(str, Enum):
    """Semantic model types for easy configuration."""

    FAST = "fast"  # Quick responses, lower cost
    SMART = "smart"  # Balanced performance and quality
    DEEP_THINKING = "deep"  # Highest quality, slower responses
    CODE = "code"  # Specialized for code generation
    ANALYSIS = "analysis"  # Specialized for analysis tasks
