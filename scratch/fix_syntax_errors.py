# fix_syntax_errors.py
import re
import os

fixes = {
    "gemini_sre_agent/llm/config_loaders.py": [
        (r"file_path: Union\[str, Path\]: str", "file_path: Union[str, Path]"),
        (r"config_data: Dict\[str, Any\]: str", "config_data: Dict[str, Any]"),
    ],
    "gemini_sre_agent/llm/mirascope_response.py": [
        (r"patterns: Dict\[str, str\]: str", "patterns: Dict[str, str]"),
    ],
    "gemini_sre_agent/llm/provider_framework/base_template.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/metrics/alerting.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/ml/workflow/workflow_analysis.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/ml/workflow/workflow_generation.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/ml/workflow/workflow_metrics.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/ml/workflow/workflow_validation.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/source_control/base.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/source_control/base_implementation.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/configured_provider.py": [
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/source_control/enhanced_base_implementation.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
        (r"default: Any : Optional\[str\] = None", "default: Any = None"),
    ],
    "gemini_sre_agent/source_control/error_handling/factory.py": [
        (r"config: Optional\[Dict\[str, Any\]\]: Optional\[str\] = None", "config: Optional[Dict[str, Any]] = None"),
    ],
    "gemini_sre_agent/source_control/health_checks.py": [
        (r"decorator\(func: Callable\[\[SourceControlProvider\], Awaitable\[HealthCheck\]\]: str\)", "decorator(func: Callable[[SourceControlProvider], Awaitable[HealthCheck]])"),
    ],
    "gemini_sre_agent/source_control/monitoring.py": [
        (r"rule_func: Callable\[\[Dict\[str, Any\]\]: str, bool\]: str", "rule_func: Callable[[Dict[str, Any]], bool]"),
        (r"handler: Callable\[\[Alert\], None\]: str", "handler: Callable[[Alert], None]"),
    ],
    "gemini_sre_agent/source_control/providers/github/enhanced_github_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/providers/github/github_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/providers/gitlab/enhanced_gitlab_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/providers/gitlab/gitlab_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/providers/local/enhanced_local_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
    "gemini_sre_agent/source_control/providers/local/local_provider.py": [
        (r"config: Dict\[str, Any\]: str", "config: Dict[str, Any]"),
    ],
}

root_dir = "/home/divyansh-rawat/Argus"

for filepath, file_fixes in fixes.items():
    full_path = os.path.join(root_dir, filepath)
    if not os.path.exists(full_path):
        print(f"Skipping {filepath} (does not exist)")
        continue
    
    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    original = content
    for pattern, replacement in file_fixes:
        content = re.sub(pattern, replacement, content)
        
    if content != original:
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Patched {filepath}")
    else:
        print(f"No changes needed for {filepath}")
