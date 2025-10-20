# MovieBrowser2 Backend

A simple backend for managing and browsing shows/movies.

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Run database migrations:

   ```bash
   alembic upgrade head
   ```

3. Run seeders

   ```bash
   python run_seeders.py
   ```

4. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

   or run main.py directly:

   ```bash
   python main.py
   ```

## Running this on the background in WSL

1. **Configure and install the service:**

   ```bash
   # Make the setup script executable
   chmod +x scripts/setup_service.sh

   # Run with default values (user: "user", home: "/home/user")
   ./scripts/setup_service.sh

   # Or specify custom values
   ./scripts/setup_service.sh myusername /home/myusername
   ```

2. **Enable and start the service:**

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable --now moviebrowser.service
   sudo systemctl status moviebrowser.service
   ```

- To stop and remove the link:
  ```bash
  sudo systemctl disable --now moviebrowser.service
  sudo systemctl daemon-reload
  # if you used systemctl link:
  sudo systemctl unlink /home/user/codes/MovieBrowser2_backend/scripts/moviebrowser.service
  # If you linked the unit with 'systemctl link', remove the created symlink manually:
  sudo rm /etc/systemd/system/moviebrowser.service
  # or if you created a manual symlink:
  sudo rm /etc/systemd/system/moviebrowser.service
  sudo systemctl daemon-reload
  ```

## Rollback

To rollback the database to the previous migration, run:

```bash
alembic downgrade -1
```

You can specify a particular revision by replacing `-1` with the desired revision identifier.

## License

MIT
