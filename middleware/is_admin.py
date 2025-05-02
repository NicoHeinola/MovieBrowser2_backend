import asyncio
from functools import wraps
from fastapi import Request, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User


def is_admin(func):
    """
    Decorator to ensure the user is authenticated and is an admin.
    """

    @wraps(func)
    async def wrapper(request: Request, db: Session = Depends(get_db), *args, **kwargs):

        try:
            user: User = request.state.user
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                )

            if not user.is_admin:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User does not have admin privileges",
                )

        except HTTPException as e:
            raise e
        except Exception as e:
            print(f"Error in is_admin middleware: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing token or checking admin status",
            )

        # Await the result if the wrapped function is async
        result = func(request=request, db=db, *args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        else:
            return result

    return wrapper
