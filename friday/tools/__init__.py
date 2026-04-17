"""
Tool registry — imports and registers all tool modules with the MCP server.
Add new tool modules here as you build them.
"""

from friday.tools import web, system, utils, google_workspace, memory, hardware, workspace


def register_all_tools(mcp):
    """Register all tool groups onto the MCP server instance."""
    web.register(mcp)
    system.register(mcp)
    utils.register(mcp)
    google_workspace.register(mcp)
    memory.register(mcp)
    hardware.register(mcp)
    workspace.register(mcp)
