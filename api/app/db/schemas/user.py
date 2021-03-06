import typing as t

from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    email: str = None
    is_active: bool = True
    is_superuser: bool = False


class UserOut(UserBase):
    pass


class UserCreate(UserBase):
    password: str

    class Config:
        orm_mode = True


class UserEdit(UserBase):
    password: t.Optional[str] = None

    class Config:
        orm_mode = True


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None
    permissions: str = "user"
