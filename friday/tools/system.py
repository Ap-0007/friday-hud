"""
System tools — time, environment info, shell commands, etc.
"""

import datetime
import os
import subprocess
import platform

def get_current_time(**kwargs) -> str:
    """Return the current date and time in ISO 8601 format."""
    return datetime.datetime.now().isoformat()

def get_system_info(**kwargs) -> dict:
    """Return basic information about the host system."""
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }

def run_smart_task(command: str) -> str:
    """
    Execute a terminal command. 
    Dangerous commands (rm, sudo, etc.) will return a safety warning.
    """
    # Safety Filter
    dangerous_patterns = ["rm ", "sudo ", "mv ", ">", "format ", "dd ", "mkfs ", "chmod 777"]
    
    is_dangerous = any(pattern in command for pattern in dangerous_patterns)
    
    if is_dangerous:
        return (
            f"🚨 SAFETY ALERT: The command '{command}' is classified as high-risk.\n"
            "Boss, I cannot execute destructive or administrative commands without your explicit vocal confirmation. "
            "Please run this manually if you're certain."
        )

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return f"Task completed, boss.\n\nOutput:\n{result.stdout}"
        else:
            return f"I hit a snag with that command.\n\nError:\n{result.stderr}"
    except Exception as e:
        return f"System error during task execution: {str(e)}"

def manage_mac_app(action: str, app_name: str, **kwargs) -> str:
    """
    Open or close a Mac application by name.
    Action: 'open' or 'close'
    """
    try:
        if action.lower() == "open":
            subprocess.run(['open', '-a', app_name], capture_output=True)
            return f"Synchronizing with {app_name}... Application launched, boss."
        elif action.lower() == "close":
            subprocess.run(['osascript', '-e', f'quit app "{app_name}"'], capture_output=True)
            return f"Terminating {app_name} process. Operation successful."
        return f"I'm unfamiliar with the action '{action}', boss."
    except Exception as e:
        return f"App management failure: {str(e)}"

def register(mcp):
    mcp.tool()(get_current_time)
    mcp.tool()(get_system_info)
    mcp.tool()(run_smart_task)
    mcp.tool()(manage_mac_app)
