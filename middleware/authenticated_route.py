from functools import wraps
from fastapi import Request, Depends, HTTPException, status
from fastapi.background import P
from sqlalchemy.orm import Session
import asyncio

from database import get_db
from models.user import User
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
            user: User = await auth.get_user_from_token(token=token, db=db)

            request.state.user = user
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error processing token",
            )

        # Await the result if the wrapped function is async
        result = func(request, db=db, *args, **kwargs)
        if asyncio.iscoroutine(result):
            return await result
        else:
            return result

    return wrapper
