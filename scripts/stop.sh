#!/bin/bash

echo "Stopping MovieBrowser Backend on port 8000..."

# Find and kill the process using port 8000
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