#!/bin/bash

# Default values
DEFAULT_SERVICE_USER="user"
DEFAULT_USER_HOME="/home/user"

# Get user input or use defaults
SERVICE_USER="${1:-$DEFAULT_SERVICE_USER}"
USER_HOME="${2:-$DEFAULT_USER_HOME}"

echo "Setting up MovieBrowser service with:"
echo "  Service User: $SERVICE_USER"
echo "  User Home: $USER_HOME"

# Clean up any existing service files or symlinks
echo "Cleaning up existing service files..."
sudo systemctl stop moviebrowser.service 2>/dev/null || true
sudo systemctl disable moviebrowser.service 2>/dev/null || true
sudo rm -f /etc/systemd/system/moviebrowser.service
sudo systemctl daemon-reload

# Create the service file with substituted values
cat > /tmp/moviebrowser.service << EOF
[Unit]
Description=MovieBrowser Backend API
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
WorkingDirectory=$USER_HOME/codes/MovieBrowser2_backend
Environment="ENVIRONMENT=production"
Environment="SQLALCHEMY_DATABASE_URL=sqlite:///./database_instance/production/database.db"
Environment="PYTHONPATH=$USER_HOME/codes/MovieBrowser2_backend"
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/snap/bin"
Environment="DISPLAY=:0"
Environment="WAYLAND_DISPLAY=wayland-0"
Environment="XDG_RUNTIME_DIR=/run/user/1000"
Environment="PULSE_RUNTIME_PATH=/run/user/1000/pulse"
ExecStartPre=/bin/mkdir -p $USER_HOME/codes/MovieBrowser2_backend/database_instance/production
ExecStartPre=/bin/bash -c 'source $USER_HOME/codes/MovieBrowser2_backend/.venv/bin/activate && alembic upgrade head'
ExecStartPre=/bin/bash -c 'source $USER_HOME/codes/MovieBrowser2_backend/.venv/bin/activate && python3 run_seeders.py'
ExecStart=/bin/bash -c 'source $USER_HOME/codes/MovieBrowser2_backend/.venv/bin/activate && python3 main.py'
Restart=always
RestartSec=10
StandardOutput=append:$USER_HOME/codes/MovieBrowser2_backend/moviebrowser.log
StandardError=append:$USER_HOME/codes/MovieBrowser2_backend/moviebrowser.log

[Install]
WantedBy=multi-user.target
EOF

# Copy directly to systemd directory
sudo cp /tmp/moviebrowser.service /etc/systemd/system/moviebrowser.service
rm /tmp/moviebrowser.service

echo "Service file created successfully!"

# Start the service
echo "Enabling and starting the MovieBrowser service..."

sudo systemctl daemon-reload
sudo systemctl enable moviebrowser.service
sudo systemctl start moviebrowser.service
sudo systemctl status moviebrowser.service