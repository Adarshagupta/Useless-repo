from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api.v1 import deps

router = APIRouter()


@router.get("/me", response_model=schemas.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    password: str = Body(None),
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    if password is not None:
        user_in.password = password
        
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user 