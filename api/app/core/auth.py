import jwt
from fastapi import Depends, HTTPException, status

import app.db.models.user as user_model
import app.db.schemas.user as user_schema
from app.core import security
from app.db import session
from app.db.crud.user import create_user, get_user_by_username


async def get_current_user(db=Depends(session.get_db), token: str = Depends(security.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        permissions: str = payload.get("permissions")
        token_data = user_schema.TokenData(username=username, permissions=permissions)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: user_model.User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_active_superuser(
    current_user: user_model.User = Depends(get_current_user),
) -> user_model.User:
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="The user doesn't have enough privileges")
    return current_user


def authenticate_user(db, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not security.verify_password(password, user.password):
        return False
    return user


def sign_up_new_user(db, username: str, password: str, email:str = None):
    user = get_user_by_username(db, username)
    if user:
        return False  # User already exists
    new_user = create_user(
        db,
        user_schema.UserCreate(
            username=username,
            email=email,
            password=password,
            is_active=True,
            is_superuser=False,
        ),
    )
    return new_user
