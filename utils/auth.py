import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from database import get_db
from models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION_SECONDS = os.getenv("ACCESS_TOKEN_EXPIRATION_SECONDS", 10)
REFRESH_TOKEN_EXPIRATION_SECONDS = os.getenv("REFRESH_TOKEN_EXPIRATION_SECONDS", 20)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(seconds=int(ACCESS_TOKEN_EXPIRATION_SECONDS))
    refresh_token_expire = datetime.now() + timedelta(seconds=int(REFRESH_TOKEN_EXPIRATION_SECONDS))

    to_encode.update({"access_token_exp": expire.timestamp(), "refresh_token_exp": refresh_token_expire.timestamp()})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    if not token:
        return None

    if token.startswith("Bearer "):
        token = token.split(" ")[1]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        return None


async def get_user_from_token(token, db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )

    try:
        payload = decode_access_token(token)

        if payload is None:
            raise credentials_exception

        expiration: float = float(payload.get("access_token_exp"))
        if expiration is None or datetime.fromtimestamp(expiration) < datetime.now():
            raise credentials_exception

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user
