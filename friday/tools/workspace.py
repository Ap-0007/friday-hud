import os
import subprocess
from typing import List, Dict, Optional
from mcp.server.fastmcp import FastMCP

# Path to the workspace
WORKSPACE_DIR = "/Users/amogh/Downloads/anti/side_pro"

# Project specific metadata
PROJECT_METADATA = {
    "indian_equities_agent": {
        "name": "EquityAgent Pro",
        "description": "Institutional-grade market intelligence terminal.",
        "url": "http://localhost:5005",
        "main_file": "simulation_engine.py"
    },
    "friday-tony-stark-demo": {
        "name": "Friday // Maya",
        "description": "Your neural assistant core.",
        "url": "http://localhost:8000",
        "main_file": "agent_friday.py"
    },
    "LunaStream": {
        "name": "LunaStream",
        "description": "High-performance screen sharing system.",
        "url": "http://localhost:5000",
        "main_file": "server.py"
    },
    "LunaRemote": {
        "name": "LunaRemote",
        "description": "Tactical remote system control.",
        "url": "http://localhost:5001",
        "main_file": "server.py"
    },
    "pulse-dashboard": {
        "name": "Project Pulse",
        "description": "Workspace health and vitality monitor.",
        "url": "http://localhost:5003",
        "main_file": "server.py"
    },
    "zenith-commander": {
        "name": "Zenith Commander",
        "description": "Sensory HUD orchestrator.",
        "url": "http://localhost:5006",
        "main_file": "server.py"
    }
}

def list_lab_projects(**kwargs) -> str:
    """
    List all projects currently in the secondary workspace (the Lab).
    Returns names and brief descriptions.
    """
    try:
        items = os.listdir(WORKSPACE_DIR)
        dirs = [i for i in items if os.path.isdir(os.path.join(WORKSPACE_DIR, i)) and not i.startswith('.')]
        
        if not dirs:
            return "The lab appears to be empty, boss."
        
        result = "Current projects in the lab:\n\n"
        for d in dirs:
            meta = PROJECT_METADATA.get(d, {"name": d, "description": "No detailed diagnostics available."})
            result += f"- {meta['name']} ({d}): {meta['description']}\n"
        
        return result
    except Exception as e:
        return f"Diagnostic failure while scanning workspace: {str(e)}"

def launch_project(project_id: str, **kwargs) -> str:
    """
    Launch a specific project by ID (directory name).
    This opens the code in VS Code and provides the launch URL if applicable.
    """
    project_path = os.path.join(WORKSPACE_DIR, project_id)
    
    if not os.path.exists(project_path):
        return f"I can't find a project with the ID '{project_id}' in the lab, boss."

    try:
        # 1. Open in VS Code
        subprocess.run(["code", project_path], check=False)
        
        # 2. Identify launch details
        meta = PROJECT_METADATA.get(project_id)
        
        response = f"Opening {project_id} in the main terminal now, boss."
        
        if meta and meta.get("url"):
            # If we have a URL, hint it
            response += f"\nI've also initialized the data downlink at {meta['url']}."
            # Attempt to open browser
            subprocess.run(["open", meta["url"]], check=False)
        
        return response
    except Exception as e:
        return f"Critical error during project initialization: {str(e)}"

def open_lab_folder(**kwargs) -> str:
    """Opens the main side_pro workspace folder in Finder."""
    try:
        subprocess.run(["open", WORKSPACE_DIR], check=False)
        return "Workspace folder is now visible on your primary display, boss."
    except Exception as e:
        return f"Failed to reveal workspace: {str(e)}"

def register(mcp):
    """Register workspace management tools."""
    mcp.tool()(list_lab_projects)
    mcp.tool()(launch_project)
    mcp.tool()(open_lab_folder)
