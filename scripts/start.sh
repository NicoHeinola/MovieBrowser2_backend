#!/bin/bash

# Auto-start MovieBrowser Backend
# Check if port 8000 is already in use
if ! lsof -i:8000 > /dev/null 2>&1; then
    cd /home/user/codes/MovieBrowser2_backend
    
    # Create necessary directories
    mkdir -p database_instance
    
    # Run migrations, seeders, and start the application in background
    echo "Starting MovieBrowser Backend..."
    nohup bash -c "
        # Set environment variables only for this process
        export ENVIRONMENT=production
        export SQLALCHEMY_DATABASE_URL=sqlite:///./database_instance/production/database.db
        export PYTHONPATH=/home/user/codes/MovieBrowser2_backend
        
        source venv/bin/activate 2>/dev/null || true
        alembic upgrade head
        python run_seeders.py
        python main.py
    " > moviebrowser.log 2>&1 &
    
    echo "MovieBrowser Backend started in background on port 8000 (check moviebrowser.log for output)"
else
    echo "MovieBrowser Backend already running on port 8000"
fi