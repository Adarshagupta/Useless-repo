from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.api.v1 import deps
from app.core import security
from app.core.config import settings
from pydantic import EmailStr
import secrets
import string

router = APIRouter()

# In-memory storage for password reset tokens (in production, use a database)
password_reset_tokens = {}

def generate_reset_token() -> str:
    # Generate a secure random token
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))

@router.post("/register", response_model=schemas.User)
def register_user(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Query(..., description="Username for the new user"),
    password: str = Query(..., description="Password for the new user"),
    email: EmailStr = Query(..., description="Email address for the new user"),
    full_name: str = Query(None, description="Full name of the user")
) -> Any:
    """
    Create new user
    """
    # Check if user with this email already exists
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    
    # Check if username is already taken
    user_by_username = crud.user.get_by_username(db, username=username)
    if user_by_username:
        raise HTTPException(
            status_code=400,
            detail="The username is already taken",
        )
    
    # Create new user
    user_in = schemas.UserCreate(
        username=username,
        password=password,
        email=email,
        full_name=full_name,
    )
    user = crud.user.create(db, obj_in=user_in)
    return user

@router.post("/login/access-token", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/login/test-token", response_model=schemas.User)
def test_token(current_user: models.User = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user

@router.post("/password-reset/request", response_model=schemas.Msg)
def request_password_reset(
    email: EmailStr = Body(...), db: Session = Depends(deps.get_db)
) -> Any:
    """
    Request a password reset token for a user
    """
    user = crud.user.get_by_email(db, email=email)
    
    # Always return success even if the email doesn't exist to prevent email enumeration
    if user and crud.user.is_active(user):
        # Generate a password reset token
        token = generate_reset_token()
        
        # Store the token with the user ID (in production, use a database table with expiration)
        password_reset_tokens[token] = user.id
        
        # In a real implementation, send an email with the reset token/link
        # Example: send_password_reset_email(email=user.email, token=token)
    
    return {"msg": "If your email is registered, you will receive a password reset link shortly"}

@router.post("/password-reset/confirm", response_model=schemas.Msg)
def confirm_password_reset(
    token: str = Body(...),
    new_password: str = Body(...),
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Reset password with a valid token
    """
    # Check if the token exists
    if token not in password_reset_tokens:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    # Get the user ID and delete the token
    user_id = password_reset_tokens.pop(token)
    
    # Get the user
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Update the user's password
    crud.user.update(db, db_obj=user, obj_in={"password": new_password})
    
    return {"msg": "Password updated successfully"}