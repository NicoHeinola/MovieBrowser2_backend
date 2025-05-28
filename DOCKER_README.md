# MovieBrowser Backend Docker Setup

This guide will help you run the MovieBrowser backend in Docker and set it up to start automatically when your PC restarts.

## Prerequisites

1. Install Docker Desktop for Windows from: https://www.docker.com/products/docker-desktop/
2. Make sure Docker Desktop is set to start on boot (Docker Desktop Settings > General > "Start Docker Desktop when you log in")
3. Enable WSL2 integration in Docker Desktop (Settings > Resources > WSL Integration)
4. Ensure your F: drive is accessible in WSL2 (it should be mounted at `/mnt/f`)

## Quick Start

1. **Build and run the container:**

   ```bash
   docker-compose up -d
   ```

2. **Check if it's running:**

   ```bash
   docker-compose ps
   ```

3. **View logs:**

   ```bash
   docker-compose logs -f
   ```

4. **Stop the container:**
   ```bash
   docker-compose down
   ```

## Auto-start Setup for Windows

### Method 1: Using Task Scheduler (Recommended)

1. Open Task Scheduler (search for "Task Scheduler" in Start menu)
2. Click "Create Basic Task..."
3. Name: "MovieBrowser Backend Auto Start"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program/script: `powershell.exe`
7. Arguments: `-ExecutionPolicy Bypass -File "c:\Users\user\Desktop\Codes\MovieBrowser2_backend\start-moviebrowser.ps1"`
8. Finish and test by restarting your computer

### Method 2: Using Windows Startup Folder

1. Press `Win + R`, type `shell:startup`, press Enter
2. Create a batch file named `start-moviebrowser.bat` with this content:
   ```batch
   @echo off
   cd /d "c:\Users\user\Desktop\Codes\MovieBrowser2_backend"
   docker-compose up -d
   ```
3. Save the file in the startup folder

### Method 3: Using Docker's Restart Policy (Already configured)

The docker-compose.yml already includes `restart: unless-stopped`, which means:

- Container will restart automatically if it crashes
- Container will start when Docker Desktop starts
- Container won't restart if you manually stop it

## Environment Configuration

Edit the `docker-compose.yml` file to change:

- Database settings
- Secret keys
- Admin credentials
- Port mappings

## Accessing the Application

Once running, your API will be available at:

- http://localhost:8000 (main API)
- http://localhost:8000/docs (Swagger documentation)

## Troubleshooting

1. **Container won't start:**

   ```bash
   docker-compose logs
   ```

2. **Database issues:**

   ```bash
   docker-compose exec moviebrowser-backend alembic upgrade head
   ```

3. **Reset everything:**

   ```bash
   docker-compose down -v
   docker-compose up -d
   ```

4. **Update the application:**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

## Data Persistence

The following directories are mounted to persist data:

- `./database_instance` - SQLite database files
- `./data` - Application data and seeders
- `/mnt/f` (F: drive) - Video files for upload and streaming (mounted at `/app/videos` inside container)

Your data will persist even if you recreate the container.

## F: Drive Access for Videos

The container is configured to mount your F: drive for video storage and access:

### WSL2 Setup

1. Ensure WSL2 is properly configured with Docker Desktop
2. Your F: drive should automatically be available at `/mnt/f` in WSL2
3. The container mounts `/mnt/f` to `/app/videos` for video access

### Verifying F: Drive Access

To verify F: drive is accessible in WSL2:

```bash
# From WSL2 terminal
ls /mnt/f
```

To test inside the Docker container:

```bash
# Check if F: drive is mounted in container
docker-compose exec moviebrowser-backend ls /app/videos

# Or start a shell inside the container
docker-compose exec moviebrowser-backend /bin/bash
```

### Video Path Configuration

- Environment variable: `VIDEO_STORAGE_PATH=/app/videos`
- Container path: `/app/videos` (maps to your F: drive)
- You can modify the volume mount in `docker-compose.yml` to use specific subdirectories:
  ```yaml
  volumes:
    - /mnt/f/Movies:/app/videos/movies
    - /mnt/f/TV_Shows:/app/videos/tv_shows
  ```

### Troubleshooting F: Drive Access

1. **F: drive not visible in WSL2:**

   ```bash
   # Check mounted drives
   mount | grep /mnt/

   # If F: drive is missing, try remounting
   sudo mkdir -p /mnt/f
   sudo mount -t drvfs F: /mnt/f
   ```

2. **Permission issues:**

   ```bash
   # Check permissions
   ls -la /mnt/f

   # If needed, you can add the following to docker-compose.yml
   user: "1000:1000"  # Adjust UID:GID as needed
   ```

3. **Container can't access videos:**
   ```bash
   # Check if volume is properly mounted
   docker-compose exec moviebrowser-backend df -h
   ```
