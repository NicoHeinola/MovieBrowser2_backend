from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.user_show_status import UserShowStatus as UserShowStatusModel
from schemas.user_show_status import UserShowStatus as UserShowStatusSchema
from middleware.authenticated_route import authenticated_route

router = APIRouter()


@router.get("/", response_model=List[UserShowStatusSchema])
@authenticated_route
def get_user_show_statuses(request: Request, show_id: Optional[int] = None, db: Session = Depends(get_db)):
    user = request.state.user
    query = db.query(UserShowStatusModel).filter(UserShowStatusModel.user_id == user.id)

    if show_id:
        query = query.filter(UserShowStatusModel.show_id == show_id)

    return query.all()


@router.post("/", response_model=UserShowStatusSchema)
@authenticated_route
def create_or_update_user_show_status(
    request: Request, user_show_status: UserShowStatusSchema, db: Session = Depends(get_db)
):
    user = request.state.user
    db_status = (
        db.query(UserShowStatusModel)
        .filter(UserShowStatusModel.user_id == user.id, UserShowStatusModel.show_id == user_show_status.show_id)
        .first()
    )

    if db_status:
        db_status.status = user_show_status.status
    else:
        db_status = UserShowStatusModel(
            user_id=user.id, show_id=user_show_status.show_id, status=user_show_status.status
        )
        db.add(db_status)

    db.commit()
    db.refresh(db_status)
    return db_status


@router.delete("/{show_id}")
@authenticated_route
def delete_user_show_status(request: Request, show_id: int, db: Session = Depends(get_db)):
    user = request.state.user
    db_status = (
        db.query(UserShowStatusModel)
        .filter(UserShowStatusModel.user_id == user.id, UserShowStatusModel.show_id == show_id)
        .first()
    )

    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")

    db.delete(db_status)
    db.commit()

    return {"ok": True}
