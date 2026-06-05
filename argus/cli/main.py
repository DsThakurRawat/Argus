import typer
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
import os
import yaml
import asyncio
from pathlib import Path

app = typer.Typer(help="👁️ Argus: Autonomous Multi-Provider Cloud SRE & AI Monitoring Assistant")
console = Console()

def print_banner():
    ascii_art = """
    █████╗ ██████╗  ██████╗ ██╗   ██╗███████╗
   ██╔══██╗██╔══██╗██╔════╝ ██║   ██║██╔════╝
   ███████║██████╔╝██║  ███╗██║   ██║███████╗
   ██╔══██║██╔══██╗██║   ██║██║   ██║╚════██║
   ██║  ██║██║  ██║╚██████╔╝╚██████╔╝███████║
   ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝  ╚═════╝ ╚══════╝
    """
    
    subtitle = Text("🤖 Autonomous Multi-Provider Cloud SRE & AI Monitoring Assistant\nObserve • Reason • Act • Heal", justify="center", style="dim")
    version = Text("\nv0.2.1\nMade by DIVYANSH RAWAT", justify="right", style="dim")
    
    content = Text(ascii_art, style="bold cyan", justify="center")
    content.append(subtitle)
    content.append(version)
    
    panel = Panel(
        content,
        title="Welcome to Argus SRE",
        border_style="cyan",
        padding=(1, 2)
    )
    console.print(panel)

@app.callback()
def main_callback():
    """Argus: Autonomous Multi-Provider Cloud SRE & AI Monitoring Assistant"""
    pass

@app.command()
def init():
    """Initialize the Argus base directory and default configurations."""
    print_banner()
    console.print("[bold green]Initializing Argus configuration...[/bold green]")
    argus_dir = Path.home() / ".argus"
    argus_dir.mkdir(exist_ok=True)
    config_file = argus_dir / "config.yaml"
    if not config_file.exists():
        with open(config_file, "w") as f:
            yaml.dump({"provider": "gemini", "bots": {}}, f)
    console.print(f"✅ Created {argus_dir} configuration directory.")

@app.command()
def run(
    log_file: str = typer.Option(None, "--log-file", "-l", help="Path to the log file to monitor"),
    provider: str = typer.Option(None, "--provider", "-p", help="LLM Provider to use (gemini, openai, etc)")
):
    """Start the Argus SRE daemon."""
    print_banner()

    import questionary
    
    custom_style = questionary.Style([
        ('qmark', 'fg:#00ffff bold'),
        ('question', 'bold'),
        ('answer', 'fg:#00ffff bold'),
        ('pointer', 'fg:#00ffff bold'),
        ('highlighted', 'fg:#aaffaa bold'), # Light green when selected
        ('selected', 'fg:#aaffaa bold'),    # Light green in checkbox
        ('text', 'fg:#aaffaa'),             # Light green for unselected
    ])
            
    cloud_platform = questionary.select(
        "Where is your project deployed? (Select log source)",
        choices=[
            "Local File System",
            "AWS (Amazon Web Services)",
            "GCP (Google Cloud Platform)",
            "Azure",
            "Vercel",
            "Render",
            "Railway",
            "Cloudflare"
        ],
        style=custom_style
    ).ask()
    if not cloud_platform:
        raise typer.Exit()

    if not provider:
        provider = questionary.select(
            "Which AI / LLM Provider do you want to use?",
            choices=["gemini", "openai", "anthropic", "ollama", "groq"],
            style=custom_style
        ).ask()
        if not provider:
            raise typer.Exit()
        
        # Ask for API Key securely
        if provider != "ollama":
            api_key = questionary.password(
                f"Enter your {provider.capitalize()} API Key (input hidden):",
                style=custom_style
            ).ask()
            if not api_key: raise typer.Exit()

    bots = questionary.checkbox(
        "Which notification bots would you like to enable? (Space to select, Enter to confirm)",
        choices=["Slack", "Discord", "Telegram"],
        style=custom_style
    ).ask()
    
    if bots is None:
        raise typer.Exit()
        
    bot_tokens = {}
    if "Slack" in bots:
        bot_tokens["slack"] = questionary.password("Enter your Slack Bot Token:", style=custom_style).ask()
    if "Discord" in bots:
        bot_tokens["discord"] = questionary.text("Enter your Discord Webhook URL:", style=custom_style).ask()
    if "Telegram" in bots:
        bot_tokens["telegram"] = questionary.password("Enter your Telegram Bot Token:", style=custom_style).ask()

    console.print(f"\n[bold cyan]Starting Argus Daemon...[/bold cyan]")
    console.print(f"Monitoring Source: [bold yellow]{cloud_platform}[/bold yellow]")
    console.print(f"Using LLM Provider: [bold yellow]{provider}[/bold yellow]")
    if bots:
        console.print(f"Active Notifications: [bold yellow]{', '.join(bots)}[/bold yellow]")
    
    # Save config
    argus_dir = Path.home() / ".argus"
    argus_dir.mkdir(exist_ok=True)
    config_file = argus_dir / "config.yaml"
    with open(config_file, "w") as f:
        yaml.dump({"provider": provider, "bots": bot_tokens}, f)

    from argus.agents.enhanced_specialized import EnhancedAnalysisAgent
    from argus.ml.caching import ContextCache
    from argus.ml.performance import PerformanceConfig
    from argus.ml.unified_workflow_orchestrator import UnifiedWorkflowOrchestrator
    from argus.llm.config_manager import ConfigManager
    
    async def _run_daemon():
        console.print("[dim]Initializing LLM agents and caches...[/dim]")
        
        llm_config_path = "config/llm_config.yaml" if os.path.exists("config/llm_config.yaml") else "examples/dogfooding/configs/llm_config.yaml"
        llm_config = ConfigManager(llm_config_path).get_config() if os.path.exists(llm_config_path) else None
        
        enhanced_agent = EnhancedAnalysisAgent(llm_config=llm_config)
        perf_config = PerformanceConfig()
        cache = ContextCache()
        
        orchestrator = UnifiedWorkflowOrchestrator(
            enhanced_agent=enhanced_agent,
            performance_config=perf_config,
            cache=cache,
            repo_path="."
        )
        
        mock_triage_packet = {
            "issue_id": "MOCK-123",
            "initial_timestamp": "2023-10-27T10:00:00Z",
            "detected_pattern": "ConnectionTimeoutError in database module",
            "preliminary_severity_score": 8,
            "affected_services": ["db-service"],
            "sample_log_entries": ["ERROR: Connection timeout connecting to postgresql://..."],
            "natural_language_summary": "Database connection timeouts are failing requests."
        }
        
        console.print("[bold green]Agent chain initialized. Processing mock log...[/bold green]")
        
        result = await orchestrator.execute_workflow(
            triage_packet=mock_triage_packet,
            historical_logs=["previous timeout 5 mins ago"],
            configs={},
            flow_id="mock-flow-1",
            enable_validation=False
        )
        
        if result.success:
            console.print("[bold green]Workflow Success![/bold green]")
            console.print(f"Generated fix:\n{result.generated_code}")
        else:
            console.print(f"[bold red]Workflow Failed: {result.error_message}[/bold red]")

    asyncio.run(_run_daemon())

@app.command()
def config():
    """Manage Argus configurations and keys interactively."""
    print_banner()
    console.print("[bold green]Argus Configuration[/bold green]")
    argus_dir = Path.home() / ".argus"
    config_file = argus_dir / "config.yaml"
    if config_file.exists():
        with open(config_file, "r") as f:
            current_config = yaml.safe_load(f)
        console.print(f"Current config:\n{yaml.dump(current_config)}")
    else:
        console.print("No config file found. Run 'argus init' first.")

if __name__ == "__main__":
    app()
