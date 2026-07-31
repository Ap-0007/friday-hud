#!/usr/bin/env python3
import os
import sys
import time
from pathlib import Path
from dotenv import load_dotenv, set_key
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.align import Align

console = Console()
ROOT_DIR = Path(__file__).parent
ENV_FILE = ROOT_DIR / ".env"

REQUIRED_KEYS = {
    "LIVEKIT_URL": "LiveKit Project URL (wss://...)",
    "LIVEKIT_API_KEY": "LiveKit API Key",
    "LIVEKIT_API_SECRET": "LiveKit API Secret",
    "GOOGLE_API_KEY": "Google Gemini API Key (AI Studio)",
    "OPENAI_API_KEY": "OpenAI API Key (for TTS)",
    "SARVAM_API_KEY": "Sarvam AI API Key (for STT)",
    "LLM_PROVIDER": "Target AI Brain (ollama, gemini, openai)",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_status():
    load_dotenv(ENV_FILE, override=True)
    status = []
    missing = []
    for key, description in REQUIRED_KEYS.items():
        val = os.getenv(key, "").strip()
        # Check if it's the placeholder from .env.example
        is_placeholder = "your-project" in val or "APIxxxx" in val or "sk_" in val and len(val) < 15
        if not val or is_placeholder:
            status.append((key, "[red]Missing/Placeholder[/red]", description))
            missing.append(key)
        else:
            masked = val[:8] + "*" * (len(val) - 8) if len(val) > 8 else "***"
            status.append((key, f"[green]Configured[/green] ({masked})", description))
    return status, missing

def display_dashboard():
    clear_screen()
    console.print(Align.center("[bold cyan]Maya COMMAND CENTER[/bold cyan]"))
    console.print(Align.center("[dim]Maya Technologies - Internal Diagnostics v1.0.0[/dim]\n"))

    status_data, missing = get_status()
    
    table = Table(title="System Configuration Status", box=None, header_style="bold magenta")
    table.add_column("Environment Variable", style="cyan")
    table.add_column("Status", justify="center")
    table.add_column("Description", style="dim")

    for key, stat, desc in status_data:
        table.add_row(key, stat, desc)

    console.print(Panel(table, border_style="blue", expand=False))

    if missing:
        console.print(f"\n[bold yellow]Attention Boss:[/bold yellow] {len(missing)} system components are offline.")
        console.print("[dim]We need those API keys to initialize the neural sensors and vocal synthesis.[/dim]")
    else:
        console.print("\n[bold green]Systems Nominal.[/bold green] All neural pathways are synchronized.")
    
    console.print("\n[bold]Main Menu:[/bold]")
    console.print("1. Configure Missing Keys")
    console.print("2. Run Health Check")
    console.print("3. Launch Instructions")
    console.print("4. [bold cyan]Launch Simulator (Terminal)[/bold cyan]")
    console.print("5. [bold blue]Launch Voice HUD (Browser - No Keys)[/bold blue]")
    console.print("6. [bold yellow]Link Google Workspace (Gmail/Classroom)[/bold yellow]")
    console.print("7. [bold green]Switch Brain (Local/Cloud)[/bold green]")
    console.print("8. Exit")
    
    choice = Prompt.ask("\nSelect operation", choices=["1", "2", "3", "4", "5", "6", "7", "8"], default="1")
    return choice

def run_setup():
    status_data, missing = get_status()
    if not missing:
        console.print("[green]All keys are already configured![/green]")
        time.sleep(1)
        return

    console.print("\n[bold cyan]Neural Pathway Sync In-Progress...[/bold cyan]")
    for key in missing:
        description = REQUIRED_KEYS[key]
        val = Prompt.ask(f"\nEnter [bold cyan]{key}[/bold cyan] ({description})")
        if val:
            set_key(str(ENV_FILE), key, val)
            console.print(f"[dim]Saved {key} to environment.[/dim]")

    console.print("\n[bold green]Environment updated successfully.[/bold green]")
    time.sleep(1)

def show_launch_instructions():
    clear_screen()
    console.print(Panel(
        "[bold cyan]MAYA TECHNOLOGIES - DEPLOYMENT PROTOCOL[/bold cyan]\n\n"
        "To initialize Maya, open two separate terminal windows:\n\n"
        "[bold white]Terminal 1 (The Brain/MCP):[/bold white]\n"
        f"[green]cd {ROOT_DIR}[/green]\n"
        "[green]~/.local/bin/uv run maya[/green]\n\n"
        "[bold white]Terminal 2 (The Voice/Agent):[/bold white]\n"
        f"[green]cd {ROOT_DIR}[/green]\n"
        "[green]~/.local/bin/uv run maya_voice[/green]\n\n"
        "[bold cyan]Interfacing:[/bold cyan]\n"
        "Connect via the [bold underline]LiveKit Agents Playground[/bold underline]\n"
        "URL: https://agents-playground.livekit.io",
        title="Deployment Instructions",
        border_style="cyan"
    ))
    input("\nPress Enter to return to Command Center...")

def main():
    if not ENV_FILE.exists():
        console.print("[yellow]Warning: .env file missing. Creating from example...[/yellow]")
        if (ROOT_DIR / ".env.example").exists():
            import shutil
            shutil.copy(str(ROOT_DIR / ".env.example"), str(ENV_FILE))
        else:
            ENV_FILE.touch()

    # Check for auto-launch flag
    if "--auto" in sys.argv:
        console.print("[bold cyan]Executing Unified Launch Sequence...[/bold cyan]")
        handle_choice("5")
        return

    while True:
        choice = display_dashboard()
        handle_choice(choice)
        if choice == "8": break

def handle_choice(choice):
    if choice == "1":
        run_setup()
    elif choice == "2":
        console.print("\n[dim]Scanning local network for MCP server...[/dim]")
        # Simple check for the server on port 8000
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex(('127.0.0.1', 8000))
        if result == 0:
            console.print("[green]Found Brain Backend (MCP) on port 8000.[/green]")
        else:
            console.print("[red]Brain Backend (MCP) is currently OFFLINE.[/red]")
        input("\nPress Enter to continue...")
    elif choice == "3":
        show_launch_instructions()
    elif choice == "4":
        console.print("\n[dim]Initializing Simulator...[/dim]")
        time.sleep(0.5)
        # Use the local uv environment to run the simulator
        os.system(f"~/.local/bin/uv run {ROOT_DIR}/maya_simulator.py")
        input("\nPress Enter to return to Command Center...")
    elif choice == "5":
        console.print("\n[dim]Activating Vocal Interface & System Link...[/dim]")
        import webbrowser
        import subprocess
        import time
        import http.server
        import socketserver
        import threading

        # 1. Determine the correct python executable (prioritize .venv)
        venv_python = ROOT_DIR / ".venv" / "bin" / "python"
        python_exe = str(venv_python) if venv_python.exists() else sys.executable
        console.print(f"[dim]Neural Launcher using: {python_exe}[/dim]")

        # 2. Start the stats bridge if not already running
        subprocess.Popen([python_exe, f"{ROOT_DIR}/stats_bridge.py"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)

        # 3. Start the MCP Server (Port 8000) for Voice Agent connectivity
        subprocess.Popen([python_exe, f"{ROOT_DIR}/server.py"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)

        # 4. Start the Local Brain API & Web server (Port 8080)
        PORT = 8080
        subprocess.Popen([python_exe, f"{ROOT_DIR}/local_brain.py"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                         start_new_session=True)

        # Wait a moment for server to boot
        time.sleep(2.5)

        hud_url = f"http://127.0.0.1:{PORT}/hud.html"
        webbrowser.open(hud_url)
        console.print(f"[green]Dashboard Online: {hud_url}[/green]")
        console.print("[yellow]Note: Allow microphone access in your browser to speak commands.[/yellow]")
        input("\nPress Enter to return to Command Center...")
    elif choice == "6":
        clear_screen()
        console.print(Panel(
            "[bold yellow]GOOGLE WORKSPACE INTEGRATION PROTOCOL[/bold yellow]\n\n"
            "To allow Maya to read your Gmail and Classroom:\n\n"
            "1. Go to [bold cyan]Google Cloud Console[/bold cyan] (console.cloud.google.com)\n"
            "2. Create a project and enable [bold]Gmail API[/bold] and [bold]Google Classroom API[/bold].\n"
            "3. Go to 'APIs & Services' -> 'Credentials'.\n"
            "4. Click 'Create Credentials' -> 'OAuth client ID' (Application type: Desktop).\n"
            "5. Download the JSON and rename it to [bold white]credentials.json[/bold white].\n"
            "6. Place it in: [italic]" + str(ROOT_DIR) + "[/italic]\n\n"
            "Once done, Maya will handle the login on first run.",
            title="Google Workspace Setup",
            border_style="yellow"
        ))
        input("\nPress Enter to return to Command Center...")
    elif choice == "7":
        clear_screen()
        current_provider = os.getenv("LLM_PROVIDER", "gemini")
        console.print(Panel(
            f"[bold cyan]NEURAL CORE SELECTOR[/bold cyan]\n\n"
            f"Current Provider: [bold white]{current_provider}[/bold white]\n\n"
            "1. [bold green]Ollama (Local - FREE)[/bold green]\n"
            "2. [bold blue]Gemini (Cloud - Google)[/bold blue]\n"
            "3. [bold white]OpenAI (Cloud - GPT-4o)[/bold white]\n\n"
            "Note: Local mode needs Ollama running + llama3.1 model.",
            title="AI Provider Settings",
            border_style="cyan"
        ))
        prov_choice = Prompt.ask("\nSelect New Provider", choices=["1", "2", "3"], default="1")
        new_prov = {"1": "ollama", "2": "gemini", "3": "openai"}[prov_choice]
        set_key(str(ENV_FILE), "LLM_PROVIDER", new_prov)
        console.print(f"\n[green]Switched brain to {new_prov}. Neural pathways updated.[/green]")
        input("\nPress Enter to return to Command Center...")
    elif choice == "8":
        console.print("\n[italic]Signing off. Stay safe, boss.[/italic]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[dim]Emergency shutdown initiated.[/dim]")
        sys.exit(0)
