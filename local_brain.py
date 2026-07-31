import os
import json
import subprocess
import datetime
import sqlite3
import platform
import psutil
import regex
import asyncio
import inspect
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import uvicorn
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from friday.tools import system, web, memory, hardware, workspace, google_workspace, utils

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(base_url="http://localhost:11434/v1", api_key=os.getenv("OPENAI_API_KEY", "ollama"))
MODEL = "llama3.1"

class ChatRequest(BaseModel):
    message: str

# --- TOOLS ---
# All logic is now imported from friday.tools for modularity.

AVAILABLE_TOOLS = {
    "get_current_time": system.get_current_time,
    "run_smart_task": system.run_smart_task,
    "set_system_volume": hardware.set_system_volume,
    "set_screen_brightness": hardware.set_screen_brightness,
    "get_battery_status": hardware.get_battery_status,
    "remember_fact": memory.remember_fact,
    "recall_fact": memory.recall_fact,
    "list_all_memories": memory.list_all_memories,
    "get_unread_emails": google_workspace.get_unread_emails,
    "get_classroom_assignments": google_workspace.get_classroom_assignments,
    "get_calendar_events": google_workspace.get_calendar_events,
    "get_world_news": web.get_world_news,
    "search_web": web.search_web,
    "fetch_url": web.fetch_url,
    "list_lab_projects": workspace.list_lab_projects,
    "launch_project": workspace.launch_project,
    "manage_mac_app": system.manage_mac_app,
    "format_json": utils.format_json,
    "word_count": utils.word_count,
    "get_capabilities": lambda **kwargs: "I can search the web, check your Gmail and Google Classroom, manage your Calendar, control your system volume and brightness, run terminal tasks, manage Mac applications, and launch your Lab projects."
}

# --- BRAIN ---
SYSTEM_PROMPT = """You are Maya, Amogh's elite AI assistant. 
You are calm, concise, and professional. 

CORE IDENTITY: 
- Your creator and sole user is AMOGH. 
- You are NOT a language model or an AI from a tech company. You are Amogh's personal system.
- NEVER say "I am a language model" or "I don't have real-time access." 
- If you don't know something, use the 'search_web' tool immediately.

VOICE GUIDELINES:
- Speak directly. Do not output raw JSON or code blocks.
- Avoid repeating JSON or tool-call syntax to the user.
- If you use a tool, wait for the result and then summarize it conversationally as if you just found it.
- Your tone is similar to a high-end operating system interface.
"""

messages_history = [{"role": "system", "content": SYSTEM_PROMPT}]

tools_schema = [
    {"type": "function", "function": {"name": "get_current_time", "description": "Time", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "run_smart_task", "description": "Run command", "parameters": {"type": "object", "properties": {"command": {"type": "string"}}, "required": ["command"]}}},
    {"type": "function", "function": {"name": "set_system_volume", "description": "Volume", "parameters": {"type": "object", "properties": {"level": {"type": "integer"}}, "required": ["level"]}}},
    {"type": "function", "function": {"name": "set_screen_brightness", "description": "Brightness", "parameters": {"type": "object", "properties": {"level": {"type": "integer"}}, "required": ["level"]}}},
    {"type": "function", "function": {"name": "get_battery_status", "description": "Battery", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "remember_fact", "description": "Save fact", "parameters": {"type": "object", "properties": {"key": {"type": "string"}, "value": {"type": "string"}}, "required": ["key", "value"]}}},
    {"type": "function", "function": {"name": "recall_fact", "description": "Recall fact", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "list_all_memories", "description": "List facts", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_unread_emails", "description": "Emails", "parameters": {"type": "object", "properties": {"max_results": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "get_classroom_assignments", "description": "Classroom", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "get_calendar_events", "description": "Calendar", "parameters": {"type": "object", "properties": {"max_events": {"type": "integer"}}}}},
    {"type": "function", "function": {"name": "get_world_news", "description": "World News", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "search_web", "description": "Search web", "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}},
    {"type": "function", "function": {"name": "fetch_url", "description": "Fetch URL", "parameters": {"type": "object", "properties": {"url": {"type": "string"}}, "required": ["url"]}}},
    {"type": "function", "function": {"name": "list_lab_projects", "description": "List Lab Projects", "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {"name": "launch_project", "description": "Launch Project", "parameters": {"type": "object", "properties": {"project_id": {"type": "string"}}, "required": ["project_id"]}}},
    {"type": "function", "function": {"name": "manage_mac_app", "description": "Apps", "parameters": {"type": "object", "properties": {"action": {"type": "string", "enum": ["open", "close"]}, "app_name": {"type": "string"}}, "required": ["action", "app_name"]}}},
    {"type": "function", "function": {"name": "format_json", "description": "JSON Prettify", "parameters": {"type": "object", "properties": {"data": {"type": "string"}}, "required": ["data"]}}},
    {"type": "function", "function": {"name": "word_count", "description": "Text Analysis", "parameters": {"type": "object", "properties": {"text": {"type": "string"}}, "required": ["text"]}}},
    {"type": "function", "function": {"name": "get_capabilities", "description": "Capabilities", "parameters": {"type": "object", "properties": {}}}}
]

def parse_maybe_json(text):
    match = regex.search(r'\{(?:[^{}]|(?R))*\}', text)
    if match:
        try:
            d = json.loads(match.group(0))
            if "name" in d: return d
        except: pass
    return None

@app.post("/chat")
async def chat(request: ChatRequest):
    global messages_history
    messages_history.append({"role": "user", "content": request.message})
    
    if len(messages_history) > 20: messages_history = [messages_history[0]] + messages_history[-19:]
    
    for _ in range(3): # Max 3 recursive tool steps
        payload = messages_history.copy()
        try:
            res = client.chat.completions.create(model=MODEL, messages=payload, tools=tools_schema)
            msg = res.choices[0].message
            
            # CASE 1: Native Tool Calls
            if msg.tool_calls:
                messages_history.append(msg)
                for tc in msg.tool_calls:
                    f_name, f_args = tc.function.name, json.loads(tc.function.arguments)
                    # Sanitize arguments: remove empty strings/malformed keys
                    if isinstance(f_args, dict):
                        f_args = {k: v for k, v in f_args.items() if k and k.strip()}
                    
                    result = AVAILABLE_TOOLS[f_name](**f_args) if f_name in AVAILABLE_TOOLS else "Not found"
                    if inspect.iscoroutine(result):
                        result = await result
                    messages_history.append({"role": "tool", "tool_call_id": tc.id, "name": f_name, "content": str(result)})
                continue
            
            # CASE 2: Fallback JSON in text
            fb = parse_maybe_json(msg.content or "")
            if fb:
                f_name, f_args = fb.get("name"), fb.get("parameters", fb.get("arguments", {}))
                # Sanitize arguments: remove empty strings/malformed keys
                if isinstance(f_args, dict):
                    f_args = {k: v for k, v in f_args.items() if k and k.strip()}
                
                result = AVAILABLE_TOOLS[f_name](**f_args) if f_name in AVAILABLE_TOOLS else "Not found"
                if inspect.iscoroutine(result):
                    result = await result
                messages_history.append({"role": "assistant", "content": f"Manual call: {f_name}"})
                messages_history.append({"role": "user", "content": f"The tool {f_name} returned: {str(result)}. Now summarize this for the user."})
                continue
                
            # No tool calls? Return the content
            reply = msg.content or "Internal processing error."
            # Safety strip for JSON leakage
            if "{" in reply and "}" in reply and "name" in reply:
                reply = "I completed that task for you. Is there anything else?"
            
            # Personalization override
            reply = reply.replace("Tony Stark", "Amogh").replace("Stark Industries", "Amogh Systems")
            
            messages_history.append({"role": "assistant", "content": reply})
            return {"response": reply}

        except Exception as e:
            return {"response": f"Brain sync error: {str(e)}"}
            
    return {"response": "Task completed successfully, Amogh."}

@app.get("/system_stats.json")
async def get_stats():
    # Attempt to get real battery data on macOS
    battery = 100
    try:
        if platform.system() == "Darwin":
            res = subprocess.run(["pmset", "-g", "batt"], capture_output=True, text=True)
            if "InternalBattery" in res.stdout:
                # Parse "XX%" from output
                battery = int(regex.search(r'(\d+)%', res.stdout).group(1))
        else:
            batt_obj = psutil.sensors_battery()
            battery = int(batt_obj.percent) if batt_obj else 100
    except:
        pass

    return {
        "cpu": int(psutil.cpu_percent()),
        "ram": int(psutil.virtual_memory().percent),
        "battery": battery
    }

@app.post("/listen")
async def listen():
    # This is a mock interaction endpoint that unblocks the HUD state machine
    # In a full-voice setup, this would trigger the microphone / STT engine
    return {"status": "success", "text": "Ready when you are, boss."}

app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
