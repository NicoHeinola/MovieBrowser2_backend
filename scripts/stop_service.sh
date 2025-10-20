#!/bin/bash

echo "Stopping MovieBrowser Backend..."

# Check if systemd service exists and is active
if systemctl is-active --quiet moviebrowser.service 2>/dev/null; then
    echo "Stopping systemd service..."
    sudo systemctl stop moviebrowser.service
    echo "MovieBrowser Backend service stopped"
else
    # Fallback: Find and kill the process using port 8000
    PID=$(lsof -ti:8000)
    
    if [ -n "$PID" ]; then
        kill $PID
        echo "Process $PID killed successfully"
        
        # Wait a moment and check if it's still running
        sleep 2
        if lsof -i:8000 > /dev/null 2>&1; then
            echo "Process still running, force killing..."
            kill -9 $PID
        fi
        
        echo "MovieBrowser Backend stopped"
    else
        echo "No process found running on port 8000"
    fi
fi