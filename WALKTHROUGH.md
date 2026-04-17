# Walkthrough - Maya Voice HUD

I have successfully transformed the Maya simulator into a **voice-activated Iron Man experience.** 

## New Features

### 1. Maya Voice HUD (`hud.html`)
A stunning web-based dashboard that feels like you're looking through Amogh's helmet.
- [x] **Zero Config Voice Recognition**: Uses the browser's native `SpeechRecognition` engine. No API keys or external servers required.
- [x] **Neural HUD UI**: Features a pulsing Arc Reactor, real-time diagnostic panels, and glassmorphic aesthetics.
- [x] **British AI Voice**: Programmed to speak back to you using the highest quality browser voice available.
- [x] **Continuous Listening**: Once initialized, Maya stays active and listens for your commands.

### 2. Command Center Integration
The Voice HUD is now integrated as **Option 5** in your Command Center.

---

## How to Launch the Voice Experience

1.  Open your terminal and run the Command Center:
    ```bash
    cd /Users/amogh/Downloads/anti/side_pro/maya-tony-stark-demo
    ~/.local/bin/uv run control_center.py
    ```
2.  Select **Option 5: Launch Voice HUD (Browser)**.
3.  Click the **"Initialize Voice Protocol"** button in your browser.
4.  **Confirm Microphone Access** if prompted.

---

## Interacting with Maya
Since this is a simulator, she is currently optimized for these types of questions:
- *"Maya, what's the news?"*
- *"Run system diagnostics."*
- *"Who are you?"*
- *"Status report."*

Enjoy your new AI assistant, boss.
