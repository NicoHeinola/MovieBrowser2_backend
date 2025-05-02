from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from middleware.authenticated_route import authenticated_route
from database import get_db
from models.user import User
from utils import auth

from schemas.user import UserCreate, Token, User as UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user_data.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = User(username=user_data.username)
    new_user.password = auth.get_password_hash(user_data.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    # Convert user.id to string for the 'sub' claim
    access_token = auth.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
@authenticated_route
# Remove current_user from parameters, access via request.state.user
def get_current_user(request: Request, db: Session = Depends(get_db)):
    current_user = getattr(request.state, "user", None)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return current_user
