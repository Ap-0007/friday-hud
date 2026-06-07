#!/usr/bin/env python3
import time
import random
import sys
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.text import Text
from rich.layout import Layout
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from rich.align import Align

console = Console()

# --- Persona Configuration ---
SYSTEM_NAME = "F.R.I.D.A.Y."
USER_NAME = "Boss"

GREETINGS = [
    "Greetings boss, you're awake late at night today. What you up to?",
    "Systems initialized. Standing by for your instructions, boss.",
    "Neural pathways connected. I've been monitoring the archives while you were out.",
    "You look like you've got a project on your mind, boss. How can I assist?"
]

CANNED_RESPONSES = {
    "news": [
        "Pulling the global feed now... Looks like Amogh Systems shares are up 4% after the clean energy summit. Also, a minor incident in Hong Kong involving some experimental tech. I've opened the world monitor for you.",
        "The world's a busy place today, boss. Major tech breakthroughs in Scandinavia and some geopolitical shifts in the Atlantic. I'm projecting the details now.",
    ],
    "system": [
        "All systems nominal. CPU at 12%, Memory usage stable. The lab's cooling system is operating at peak efficiency.",
        "Diagnostic complete. No anomalies detected in the local grid. Your laptop's integrity is at 98%. That 2% is mostly just dust, boss.",
    ],
    "market": [
        "Markets had a decent session today, boss — tech led the gains, energy was a little soft. Nothing alarming.",
        "Indices are looking healthy. Amogh Systems is still the top performer, naturally.",
    ],
    "default": [
        "I'm on it, boss. Just checking the archives.",
        "Interesting query. Let me cross-reference that with our local database.",
        "I'll have that for you in a heartbeat. Anything else while I'm at it?",
        "Affirmative. Processing that request via our internal logic.",
    ]
}

def typewriter_print(text, speed=0.03):
    """Simulates a high-tech typing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

def simulate_boot():
    """Plays a dramatic Amogh-style boot sequence."""
    with Progress(
        SpinnerColumn(spinner_name="dots12"),
        TextColumn("[bold cyan]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Initializing Neural Core...", total=None)
        time.sleep(1)
        progress.add_task(description="Syncing Satellite Uplink...", total=None)
        time.sleep(0.8)
        progress.add_task(description="Loading Vocal Synthesis...", total=None)
        time.sleep(1.2)
        progress.add_task(description="Authenticating Boss...", total=None)
        time.sleep(0.5)

    console.print(Align.center(Panel(
        "[bold cyan]F.R.I.D.A.Y. INTERFACE ONLINE[/bold cyan]\n"
        "[dim]Iron Man Simulator Mode (No API Keys Required)[/dim]",
        border_style="blue",
        padding=(1, 2)
    )))
    time.sleep(0.5)
    
    greeting = random.choice(GREETINGS)
    console.print(f"\n[bold magenta]{SYSTEM_NAME}:[/bold magenta] ", end="")
    typewriter_print(greeting)

def get_response(user_input):
    """Simple keyword-based response engine that acts like FRIDAY."""
    user_input = user_input.lower()
    
    if any(word in user_input for word in ["news", "happening", "brief"]):
        return random.choice(CANNED_RESPONSES["news"])

    if any(word in user_input for word in ["system", "diagnostic", "status"]):
        return random.choice(CANNED_RESPONSES["system"])

    if any(word in user_input for word in ["market", "stock", "price"]):
        return random.choice(CANNED_RESPONSES["market"])

    if any(word in user_input for word in ["hello", "hi", "hey"]):
        return "Hello boss. Ready to build something incredible?"

    if any(word in user_input for word in ["who are you", "what are you"]):
        return "I'm F.R.I.D.A.Y. — Fully Responsive Intelligent Digital Assistant for You. At your service, always."

    return random.choice(CANNED_RESPONSES["default"])

def main():
    simulate_boot()
    
    while True:
        try:
            user_input = Prompt.ask(f"\n[bold green]{USER_NAME}[/bold green]")
            
            if user_input.lower() in ["exit", "stop", "shutdown", "quit"]:
                console.print(f"\n[bold magenta]{SYSTEM_NAME}:[/bold magenta] ", end="")
                typewriter_print("Shutting down. Get some rest, boss. I'll keep an eye on the lab.")
                break
                
            # Simulate "thinking"
            with console.status("[dim]Processing...[/dim]", spinner="bouncingBall"):
                time.sleep(random.uniform(0.5, 1.5))
            
            response = get_response(user_input)
            console.print(f"[bold magenta]{SYSTEM_NAME}:[/bold magenta] ", end="")
            typewriter_print(response)
            
        except KeyboardInterrupt:
            print("\n")
            main_exit()
            break

def main_exit():
    console.print(f"\n[bold magenta]{SYSTEM_NAME}:[/bold magenta] [dim]Emergency shutdown. Logged out.[/dim]")

if __name__ == "__main__":
    main()
