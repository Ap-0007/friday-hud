import json

def format_json(data: str, **kwargs) -> str:
    """Pretty-print a JSON string."""
    try:
        # If it's already a dict/list, just dump it
        if isinstance(data, (dict, list)):
            return json.dumps(data, indent=2)
        parsed = json.loads(data)
        return json.dumps(parsed, indent=2)
    except Exception as e:
        return f"Invalid JSON or parsing error: {e}"

def word_count(text: str, **kwargs) -> dict:
    """Count words, characters, and lines in a block of text."""
    lines = text.splitlines()
    words = text.split()
    return {
        "characters": len(text),
        "words": len(words),
        "lines": len(lines),
    }

def register(mcp):
    mcp.tool()(format_json)
    mcp.tool()(word_count)
