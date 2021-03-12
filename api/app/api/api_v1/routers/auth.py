from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

import app.db.models.user as user_model
from app.core import security
from app.core.auth import authenticate_user, sign_up_new_user
from app.db.session import get_db

auth_router = r = APIRouter(tags=["auth"])


def create_user_token(user: user_model.User):
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    if user.is_superuser:
        permissions = "admin"
    else:
        permissions = "user"
    access_token = security.create_access_token(
        data={"sub": user.username, "permissions": permissions},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@r.post("/token", summary="Refresh user token when login")
async def login(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_user_token(user)


@r.post("/signup", summary="Signup new non-super user")
async def signup(db=Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = sign_up_new_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already exists",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return create_user_token(user)
