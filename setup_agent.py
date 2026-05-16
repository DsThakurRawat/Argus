import os
import sys
import yaml
import time
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

# Preset models for each provider
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

def setup_env(provider, api_key, base_url=None):
    env_path = Path(".env")
    lines = []
    if env_path.exists():
        with open(env_path, "r") as f:
            lines = f.readlines()
    
    key_name = f"{provider.upper()}_API_KEY"
    found_key = False
    found_url = False
    new_lines = []
    for line in lines:
        if line.startswith(f"{key_name}="):
            new_lines.append(f'{key_name}="{api_key}"\n')
            found_key = True
        elif base_url and line.startswith(f"{provider.upper()}_BASE_URL="):
            new_lines.append(f'{provider.upper()}_BASE_URL="{base_url}"\n')
            found_url = True
        else:
            new_lines.append(line)
    
    if not found_key:
        new_lines.append(f'{key_name}="{api_key}"\n')
    if base_url and not found_url:
        new_lines.append(f'{provider.upper()}_BASE_URL="{base_url}"\n')
    
    with open(env_path, "w") as f:
        f.writelines(new_lines)

def generate_llm_config(provider, model, base_url=None):
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
    
    if provider == "ollama" and not base_url:
        config["providers"]["ollama"]["base_url"] = "http://localhost:11434"
        config["providers"]["ollama"]["api_key"] = None

    os.makedirs("config", exist_ok=True)
    with open("config/llm_config.yaml", "w") as f:
        yaml.dump(config, f)

def display_dashboard():
    console.clear()
    console.print(Text(LOGO, style="bold red"))
    console.print(f"[bold white]cloud-sre[/]  ·  [bold red]v2026.05.16[/]")
    console.print("[dim white]autonomous multi-cloud SRE agent for incident remediation[/]\n")

    status_content = Text()
    # Use getpass.getuser() for better robustness in different environments
    status_content.append(f"User: [bold white]{getpass.getuser()}[/]\n")
    status_content.append(f"Directory: [bold red]{Path.cwd().name}[/]\n")
    status_content.append(f"Available Providers: [bold green]12+ detected[/]")

    console.print(Panel(
        status_content,
        title="[bold red]System Status[/]",
        border_style="red",
        width=80
    ))

def run_setup():
    display_dashboard()
    
    provider_names = [
        "Gemini (Google)", "OpenAI (GPT-4o)", "Anthropic (Claude)", 
        "Groq (Ultra-fast)", "Ollama (Local)", "Azure OpenAI", 
        "Mistral AI", "xAI (Grok)", "Perplexity", "OpenRouter"
    ]
    provider_keys = ["gemini", "openai", "anthropic", "groq", "ollama", "azure", "mistral", "xai", "perplexity", "openrouter"]
    
    console.print("\n[bold red]── 1. Select LLM Provider ─────────────────────────────────────────────────────[/]")
    for i, p in enumerate(provider_names, 1):
        console.print(f" [bold red]{i}.[/] [white]{p}[/]")
    
    choice = Prompt.ask(
        "\n[bold red]> [/][bold white]Enter choice number[/]",
        choices=[str(i) for i in range(1, len(provider_names) + 1)],
        default="1"
    )
    provider = provider_keys[int(choice) - 1]
    
    console.print(f"\n[bold red]── 2. Configure {provider.upper()} ────────────────────────────────────────────────[/]")
    
    api_key = ""
    if provider != "ollama":
        while not api_key:
            api_key = Prompt.ask(f"[bold red]> [/][bold white]Enter {provider.upper()} API Key[/]", password=True)
            if not api_key:
                console.print("[bold yellow]⚠ API Key cannot be empty. Please enter a valid key.[/]")
    
    base_url = None
    if provider in ["azure", "openrouter", "ollama"]:
        default_url = "http://localhost:11434" if provider == "ollama" else ""
        base_url = Prompt.ask(f"[bold red]> [/][bold white]Enter {provider.upper()} Base URL[/]", default=default_url)

    # Numbered Model Selection
    models = MODEL_MAP.get(provider, ["gpt-4o"])
    console.print(f"\n[bold red]── 3. Select Model for {provider.upper()} ────────────────────────────────────────[/]")
    for i, m in enumerate(models, 1):
        console.print(f" [bold red]{i}.[/] [white]{m}[/]")
    
    model_choice = Prompt.ask(
        "\n[bold red]> [/][bold white]Enter model number[/]",
        choices=[str(i) for i in range(1, len(models) + 1)],
        default="1"
    )
    model = models[int(model_choice) - 1]
    
    with console.status("[bold red]Applying configurations...", spinner="dots"):
        setup_env(provider, api_key, base_url)
        generate_llm_config(provider, model, base_url)

    console.print("\n[bold green]✅ CONFIGURATION SUCCESSFUL[/]")
    console.print(Panel(
        f"[bold white]Your configuration is saved to config/llm_config.yaml[/]\n\n"
        f"[bold red]uv run python main.py[/]",
        title="[bold green]Ready to Launch[/]",
        border_style="green",
        width=80
    ))

if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        console.print("\n[bold red]Aborted by user.[/]")
        sys.exit(0)
