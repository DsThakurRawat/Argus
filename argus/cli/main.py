import asyncio
import os
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import typer
import yaml

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

    subtitle = Text(
        "🤖 Autonomous Multi-Provider Cloud SRE & AI Monitoring Assistant\nObserve • Reason • Act • Heal",
        justify="center",
        style="dim",
    )
    version = Text("\nv0.2.1\nMade by DIVYANSH RAWAT", justify="right", style="dim")

    content = Text(ascii_art, style="bold cyan", justify="center")
    content.append(subtitle)
    content.append(version)

    panel = Panel(content, title="Welcome to Argus SRE", border_style="cyan", padding=(1, 2))
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
    provider: str = typer.Option(
        None, "--provider", "-p", help="LLM Provider to use (gemini, openai, etc)"
    ),
):
    """Start the Argus SRE daemon."""
    print_banner()

    import questionary

    custom_style = questionary.Style(
        [
            ("qmark", "fg:#00ffff bold"),
            ("question", "bold"),
            ("answer", "fg:#00ffff bold"),
            ("pointer", "fg:#00ffff bold"),
            ("highlighted", "fg:#aaffaa bold"),  # Light green when selected
            ("selected", "fg:#aaffaa bold"),  # Light green in checkbox
            ("text", "fg:#aaffaa"),  # Light green for unselected
        ]
    )

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
            "Cloudflare",
        ],
        style=custom_style,
    ).ask()
    if not cloud_platform:
        raise typer.Exit()

    if not provider:
        provider = questionary.select(
            "Which AI / LLM Provider do you want to use?",
            choices=["gemini", "openai", "anthropic", "ollama", "groq"],
            style=custom_style,
        ).ask()
        if not provider:
            raise typer.Exit()

        # Ask for API Key securely
        if provider != "ollama":
            api_key = questionary.password(
                f"Enter your {provider.capitalize()} API Key (input hidden):", style=custom_style
            ).ask()
            if not api_key:
                raise typer.Exit()

    bots = questionary.checkbox(
        "Which notification bots would you like to enable? (Space to select, Enter to confirm)",
        choices=["Slack", "Discord", "Telegram"],
        style=custom_style,
    ).ask()

    if bots is None:
        raise typer.Exit()

    bot_tokens = {}
    if "Slack" in bots:
        bot_tokens["slack"] = questionary.text(
            "Enter your Slack Webhook URL:", style=custom_style
        ).ask()
    if "Discord" in bots:
        bot_tokens["discord"] = questionary.text(
            "Enter your Discord Webhook URL:", style=custom_style
        ).ask()
    if "Telegram" in bots:
        bot_tokens["telegram"] = questionary.password(
            "Enter your Telegram Token and Chat ID (format bot_token:chat_id):", style=custom_style
        ).ask()

    console.print("\n[bold cyan]Starting Argus Daemon...[/bold cyan]")
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

    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
    from argus.notifications.notifier import notify
    from main import run_pipeline

    async def _run_daemon():
        console.print("[dim]Initializing LLM agents and caches...[/dim]")

        # We pass provider to run_pipeline.
        # run_pipeline will start the log manager and process logs.
        # Since we don't have a real log source passed from CLI yet (it defaults to mock),
        # run_pipeline can just run the initialization and process one mock log,
        # or we can pass a mock_packet to the Notifier directly.

        mock_packet = await run_pipeline(provider_override=provider)

        if bot_tokens and mock_packet:
            console.print("[dim]Sending notifications...[/dim]")
            await notify(mock_packet, {"bots": bot_tokens})
            console.print("[bold green]Notifications sent![/bold green]")

    asyncio.run(_run_daemon())


@app.command()
def config():
    """Manage Argus configurations and keys interactively."""
    print_banner()
    console.print("[bold green]Argus Configuration[/bold green]")
    argus_dir = Path.home() / ".argus"
    config_file = argus_dir / "config.yaml"
    if config_file.exists():
        with open(config_file) as f:
            current_config = yaml.safe_load(f)
        console.print(f"Current config:\n{yaml.dump(current_config)}")
    else:
        console.print("No config file found. Run 'argus init' first.")


if __name__ == "__main__":
    app()
