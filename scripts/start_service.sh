#!/bin/bash

# Auto-start MovieBrowser Backend
echo "Starting MovieBrowser Backend..."

# Check if systemd service exists
if systemctl list-unit-files moviebrowser.service &>/dev/null; then
    # Use systemd service
    if systemctl is-active --quiet moviebrowser.service; then
        echo "MovieBrowser Backend service is already running"
        sudo systemctl status moviebrowser.service --no-pager
    else
        echo "Starting systemd service..."
        sudo systemctl start moviebrowser.service
        sleep 2
        if systemctl is-active --quiet moviebrowser.service; then
            echo "MovieBrowser Backend service started successfully"
            sudo systemctl status moviebrowser.service --no-pager
        else
            echo "Failed to start service. Check logs with: sudo journalctl -u moviebrowser -n 50"
        fi
    fi
fi