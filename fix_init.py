import os
import re

files_to_fix = [
    "argus/llm/provider_framework/auto_registry.py",
    "argus/llm/provider_framework/capability_discovery.py",
    "argus/llm/provider_framework/plugin_loader.py",
    "argus/llm/service_metrics.py",
    "argus/llm/strategy_metrics.py",
    "argus/llm/testing/benchmark_monitors.py",
    "argus/ml/base_code_generator.py",
    "argus/resilience/error_classifier.py",
    "argus/security/access_control.py",
    "argus/source_control/error_handling/classification_algorithms.py",
    "argus/source_control/error_handling/custom_fallback_strategies.py",
    "argus/source_control/error_handling/error_types.py",
    "argus/source_control/health_checks.py",
    "argus/source_control/monitoring.py"
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            content = f.read()
        
        # Replace def __init__(...) -> Any: with -> None:
        new_content = re.sub(r'(def __init__\([^)]*\)\s*)->\s*Any:', r'\1-> None:', content)
        
        with open(file_path, "w") as f:
            f.write(new_content)
        print(f"Fixed {file_path}")
    else:
        print(f"File not found: {file_path}")
