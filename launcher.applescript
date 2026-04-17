tell application "Terminal"
    do script "echo 'Initializing Maya System 2.0...' && cd /Users/amogh/Downloads/anti/side_pro/friday-tony-stark-demo && ~/.local/bin/uv run python local_brain.py"
    activate
end tell

delay 5
open location "http://127.0.0.1:8080/hud.html"
