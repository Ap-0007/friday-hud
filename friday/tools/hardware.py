"""
Hardware tools — physical system control for Mac (Volume, Brightness, Battery).
"""

import subprocess
import os

def run_osascript(script: str) -> str:
    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True, timeout=5)
        return result.stdout.strip()
    except Exception as e:
        return f"Error executing AppleScript: {str(e)}"

def set_system_volume(level: int, **kwargs) -> str:
    """
    Set the Mac system volume (0-100).
    """
    if not (0 <= level <= 100):
        return "Boss, volume must be between 0 and 100."
    
    run_osascript(f"set volume output volume {level}")
    return f"Volume adjusted to {level}%, boss."

def set_screen_brightness(level: int, **kwargs) -> str:
    """
    Set the screen brightness. Level is relative (requires simulating key presses).
    """
    if level > 50:
        script = 'tell application "System Events" to repeat 5 times\nkey code 144\nend repeat'
        msg = "Increasing brightness, boss."
    else:
        script = 'tell application "System Events" to repeat 5 times\nkey code 145\nend repeat'
        msg = "Dimming the display, boss."
    
    run_osascript(script)
    return msg

def get_battery_status(**kwargs) -> str:
    """
    Get the current battery level and charging status.
    """
    import psutil
    battery = psutil.sensors_battery()
    if not battery:
        return "I'm not detecting a battery, boss. Are we on a desktop?"
    
    percent = battery.percent
    status = "charging" if battery.power_plugged else "discharging"
    return f"Power levels are at {percent}%. We are currently {status}."

def register(mcp):
    mcp.tool()(set_system_volume)
    mcp.tool()(set_screen_brightness)
    mcp.tool()(get_battery_status)
