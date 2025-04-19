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

## API

- `GET /shows` - List all shows
- `POST /shows` - Add a new show

## License

MIT
