from functools import wraps
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from utils import auth


def authenticated_route(func):
    @wraps(func)
    async def wrapper(request: Request, db: Session = Depends(get_db), *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not authenticated",
            )

        token = auth_header.split(" ")[1]

        try:
            user = await auth.get_user_from_token(token=token, db=db)
            # Inject the user into the kwargs for the route function
            kwargs["current_user"] = user
        except HTTPException as e:
            raise e
        except Exception as e:
            # Catch any other unexpected errors during token processing
            print(f"Error during token processing: {e}")  # Add logging for debugging
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing token",
            )

        return await func(request=request, db=db, *args, **kwargs)

    return wrapper
