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
            
    if not provider:
        provider = questionary.select(
            "Which LLM Provider should power the agents?",
            choices=["gemini", "openai", "anthropic", "ollama", "groq"]
        ).ask()
        if not provider:
            raise typer.Exit()
            
    if not log_file:
        log_file = questionary.path(
            "Enter the path to the log file to monitor:"
        ).ask()
        if not log_file:
            raise typer.Exit()

    console.print(f"\n[bold cyan]Starting Argus Daemon...[/bold cyan]")
    if provider:
        console.print(f"Using LLM Provider: [bold yellow]{provider}[/bold yellow]")
    if log_file:
        console.print(f"Monitoring Log File: [bold yellow]{log_file}[/bold yellow]")
    
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
