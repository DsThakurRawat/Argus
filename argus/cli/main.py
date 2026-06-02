import typer
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

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
    
    content = Text(ascii_art, style="bold red", justify="center")
    content.append(subtitle)
    content.append(version)
    
    panel = Panel(
        content,
        title="Welcome to Argus SRE",
        border_style="red",
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
    # Setup ~/.argus directory logic here
    console.print("✅ Created ~/.argus configuration directory.")

@app.command()
def run(
    log_file: str = typer.Option(None, "--log-file", "-l", help="Path to the log file to monitor"),
    provider: str = typer.Option(None, "--provider", "-p", help="LLM Provider to use (gemini, openai, etc)")
):
    """Start the Argus SRE daemon."""
    print_banner()

    import questionary
            
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
        ]
    ).ask()
    if not cloud_platform:
        raise typer.Exit()

    if not provider:
        provider = questionary.select(
            "Which AI / LLM Provider do you want to use?",
            choices=["gemini", "openai", "anthropic", "ollama", "groq"]
        ).ask()
        if not provider:
            raise typer.Exit()
        
        # Ask for API Key securely
        if provider != "ollama":
            api_key = questionary.password(f"Enter your {provider.capitalize()} API Key (input hidden):").ask()
            if not api_key: raise typer.Exit()

    bots = questionary.checkbox(
        "Which notification bots would you like to enable? (Space to select, Enter to confirm)",
        choices=["Slack", "Discord", "Telegram"]
    ).ask()
    
    if bots is None:
        raise typer.Exit()
        
    bot_tokens = {}
    if "Slack" in bots:
        bot_tokens["slack"] = questionary.password("Enter your Slack Bot Token:").ask()
    if "Discord" in bots:
        bot_tokens["discord"] = questionary.text("Enter your Discord Webhook URL:").ask()
    if "Telegram" in bots:
        bot_tokens["telegram"] = questionary.password("Enter your Telegram Bot Token:").ask()

    console.print(f"\n[bold cyan]Starting Argus Daemon...[/bold cyan]")
    console.print(f"Monitoring Source: [bold yellow]{cloud_platform}[/bold yellow]")
    console.print(f"Using LLM Provider: [bold yellow]{provider}[/bold yellow]")
    if bots:
        console.print(f"Active Notifications: [bold yellow]{', '.join(bots)}[/bold yellow]")
    
    # Daemon logic connection here
    console.print("\n[dim]Watching for events... (Press Ctrl+C to exit)[/dim]")

@app.command()
def config():
    """Manage Argus configurations and keys interactively."""
    print_banner()
    console.print("[bold green]Argus Configuration[/bold green]")
    # Interactive prompt logic here
    console.print("Configuration feature coming soon.")

if __name__ == "__main__":
    app()
