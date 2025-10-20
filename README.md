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

1. Open `scripts/moviebrowser.service` and set `SERVICE_USER` and `USER_HOME` correctly.

2. Create a system link (two options — use one):

   - Using a manual symlink (preferred):

     ```bash
     sudo ln -s /home/user/codes/MovieBrowser2_backend/scripts/moviebrowser.service /etc/systemd/system/moviebrowser.service
     ```

   - Using systemctl:
     ```bash
     sudo systemctl link /home/user/codes/MovieBrowser2_backend/scripts/moviebrowser.service
     ```

3. Reload systemd, enable and start the service:

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
