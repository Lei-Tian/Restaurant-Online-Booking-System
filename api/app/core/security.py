
import os
import typing as t
from datetime import datetime, timedelta

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from passlib.context import CryptContext

from app.core import security
from app.db import session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/token",
    scopes={
        "server_management": "Edit server settings",
        "token_management": "Create, list or edit tokens",
        "notification_management": "Create, list or edit notification providers",
        "full_control": "Full control over what current user has",
    },
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "c3d9914e58b42bc9e30a81abe7d56f349fe58ec5a101d69ac067019eb0f82b17",
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class AuthDependency:
    def __init__(self, enabled: bool = True, token: t.Optional[str] = None):
        self.enabled = enabled
        self.token = token

    def raise_unauthorized_exception(self, authenticate_value):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )

    def raise_forbidden_exception(self, authenticate_value):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )

    async def __call__(
        self,
        request: Request,
        security_scopes: SecurityScopes,
        db=Depends(session.get_db),
    ):
        from app.api.api_v1.crud.user import get_user_by_username

        if not self.enabled:
            return None
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        token: str = await oauth2_scheme(request) if not self.token else self.token
        if token is None:
            self.raise_unauthorized_exception(authenticate_value)
        try:
            payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
        except (jwt.PyJWTError, jwt.ExpiredSignatureError):
            self.raise_unauthorized_exception(authenticate_value)
        username: str = payload.get("sub")
        permission: str = payload.get("permissions")
        user = get_user_by_username(db, username)
        if user is None:
            self.raise_forbidden_exception(authenticate_value)
        if permission is None or permission not in ["admin", "user"]:
            self.raise_forbidden_exception(authenticate_value)
        return user
