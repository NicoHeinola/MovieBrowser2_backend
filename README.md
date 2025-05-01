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

3. Start the server:

   ```bash
   uvicorn main:app --reload
   ```

   or run main.py directly:

   ```bash
   python main.py
   ```

## Rollback

To rollback the database to the previous migration, run:

```bash
alembic downgrade -1
```

You can specify a particular revision by replacing `-1` with the desired revision identifier.

## API

- `GET /shows` - List all shows
- `POST /shows` - Add a new show

## License

MIT
