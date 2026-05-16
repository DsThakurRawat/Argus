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

"""
Interactive setup dashboard for the Cloud-SRE Agent.

This script provides a premium CLI experience for configuring LLM providers,
models, and environment variables.
"""

import os
import sys
import yaml
import getpass
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

console = Console()

LOGO = """
 ██████ ██       ██████  ██    ██ ██████      ███████ ██████  ███████ 
██      ██      ██    ██ ██    ██ ██   ██     ██      ██   ██ ██      
██      ██      ██    ██ ██    ██ ██   ██     ███████ ██████  █████   
██      ██      ██    ██ ██    ██ ██   ██          ██ ██   ██ ██      
 ██████ ███████  ██████   ██████  ██████      ███████ ██   ██ ███████ 
"""

MODEL_MAP = {
    "gemini": ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-1.0-pro"],
    "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo"],
    "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
    "groq": ["llama3-70b-8192", "llama3-8b-8192", "mixtral-8x7b-32768"],
    "ollama": ["llama3.1:8b", "llama3.1:70b", "mistral", "codellama"],
    "azure": ["gpt-4o", "gpt-35-turbo"],
    "mistral": ["mistral-large-latest", "mistral-medium-latest", "open-mixtral-8x22b"],
    "xai": ["grok-beta", "grok-2"],
    "perplexity": ["llama-3-sonar-large-32k-online", "llama-3-sonar-small-32k-chat"],
    "openrouter": ["anthropic/claude-3.5-sonnet", "google/gemini-pro-1.5", "meta-llama/llama-3-70b-instruct"]
}

def safe_input(prompt_text, choices=None, default=None, password=False):
    """
    Safely handle user input with rich prompts and error recovery.

    Args:
        prompt_text: Text to display to the user.
        choices: Optional list of valid input choices.
        default: Default value if input is empty.
        password: If True, mask the input.

    Returns:
        The validated user input string.
    """
    try:
        if choices:
            return Prompt.ask(prompt_text, choices=choices, default=default, password=password)
        return Prompt.ask(prompt_text, default=default, password=password)
    except (EOFError, KeyboardInterrupt):
        console.print("\n[bold red]⚠ Setup aborted.[/]")
        sys.exit(0)

def setup_env(provider, api_key, base_url=None):
    """
    Update the .env file with the chosen provider's credentials.

    Args:
        provider: Name of the LLM provider.
        api_key: User provided API key.
        base_url: Optional base URL for the provider.
    """
    env_path = Path(".env")
    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    key_name = f"{provider.upper()}_API_KEY"
    new_lines = [l for l in lines if not l.startswith(f"{key_name}=") and not (base_url and l.startswith(f"{provider.upper()}_BASE_URL="))]
    new_lines.append(f'{key_name}="{api_key}"\n')
    if base_url:
        new_lines.append(f'{provider.upper()}_BASE_URL="{base_url}"\n')
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)

def generate_llm_config(provider, model, base_url=None):
    """
    Generate the llm_config.yaml file based on user selection.

    Args:
        provider: Selected provider name.
        model: Selected model name.
        base_url: Optional base URL.
    """
    config = {
        "default_provider": provider,
        "default_model_type": "smart",
        "enable_fallback": True,
        "providers": {
            provider: {
                "provider": provider,
                "api_key": f"${{{provider.upper()}_API_KEY}}",
                "base_url": base_url,
                "models": {
                    model: {
                        "name": model,
                        "model_type": "smart",
                        "max_tokens": 4096
                    }
                }
            }
        },
        "agents": {
            "analysis_agent": {"primary_provider": provider},
            "triage_agent": {"primary_provider": provider},
            "remediation_agent": {"primary_provider": provider}
        }
    }
    os.makedirs("config", exist_ok=True)
    with open("config/llm_config.yaml", "w") as f:
        yaml.dump(config, f)

def run_setup():
    """Execute the interactive setup dashboard."""
    console.clear()
    console.print(Text(LOGO, style="bold red"))
    console.print(f"[bold white]cloud-sre[/]  ·  [bold red]v2026.05.16[/]\n")

    status = Text()
    status.append(f"User: [bold white]{getpass.getuser()}[/]\n")
    status.append(f"System: [bold green]Ready for Configuration[/]")
    console.print(Panel(status, title="[bold red]Dashboard Status[/]", border_style="red", width=80))

    provider_keys = ["gemini", "openai", "anthropic", "groq", "ollama", "azure", "mistral", "xai", "perplexity", "openrouter"]
    for i, p in enumerate(provider_keys, 1):
        console.print(f" [bold red]{i}.[/] [white]{p.upper()}[/]")
    
    choice = safe_input("\n[bold red]> [/][bold white]Select Provider[/]", choices=[str(i) for i in range(1, 11)], default="1")
    provider = provider_keys[int(choice) - 1]

    api_key = ""
    if provider != "ollama":
        while True:
            api_key = safe_input(f"[bold red]> [/][bold white]Enter {provider.upper()} API Key[/]", password=True)
            if not api_key:
                console.print("[bold yellow]⚠ API Key cannot be empty.[/]")
                continue
            if len(api_key) < 20:
                console.print("[bold yellow]⚠ API Key looks suspiciously short.[/]")
                if safe_input("[bold red]> [/][bold white]Continue anyway? (y/n)[/]", choices=["y", "n"], default="n") != "y":
                    continue
            break

    base_url = None
    if provider in ["azure", "openrouter", "ollama"]:
        base_url = safe_input(f"[bold red]> [/][bold white]Enter Base URL[/]", default="http://localhost:11434" if provider == "ollama" else "")

    models = MODEL_MAP.get(provider, ["gpt-4o"])
    for i, m in enumerate(models, 1):
        console.print(f" [bold red]{i}.[/] [white]{m}[/]")
    m_choice = safe_input("\n[bold red]> [/][bold white]Select Model[/]", choices=[str(i) for i in range(1, len(models) + 1)], default="1")
    model = models[int(m_choice) - 1]

    with console.status("[bold red]Saving configuration...", spinner="dots"):
        setup_env(provider, api_key, base_url)
        generate_llm_config(provider, model, base_url)

    console.print("\n[bold green]✅ CONFIGURATION SUCCESSFUL[/]")

if __name__ == "__main__":
    run_setup()
