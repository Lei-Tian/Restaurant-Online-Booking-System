
import typing as t

from fastapi import APIRouter, Depends, Request, Response

from app.api.api_v1.crud.user import (
    create_user,
    delete_user,
    edit_user,
    get_user,
    get_users,
)
from app.api.api_v1.schemas.user import User, UserCreate, UserEdit
from app.core.auth import get_current_active_superuser

users_router = r = APIRouter()


@r.get(
    "/users",
    response_model=t.List[User],
    response_model_exclude_none=True,
)
async def users_list(
    request: Request,
    response: Response,
    current_user=Depends(get_current_active_superuser),
):
    """
    Get all users
    """
    users = get_users(request.state.db)
    # This is necessary for react-admin to work
    response.headers["Content-Range"] = f"0-9/{len(users)}"
    return users


@r.get("/users/me", response_model=User, response_model_exclude_none=True)
async def user_me(request: Request):
    """
    Get own user
    """
    return request.state.current_active_user


@r.get(
    "/users/{user_id}",
    response_model=User,
    response_model_exclude_none=True,
)
async def user_details(
    request: Request,
    user_id: int,
    current_user=Depends(get_current_active_superuser),
):
    """
    Get any user details
    """
    user = get_user(request.state.db, user_id)
    return user
    # return encoders.jsonable_encoder(
    #     user, skip_defaults=True, exclude_none=True,
    # )


@r.post("/users", response_model=User, response_model_exclude_none=True)
async def user_create(
    request: Request,
    user: UserCreate,
    current_user=Depends(get_current_active_superuser),
):
    """
    Create a new user
    """
    return create_user(request.state.db, user)


@r.put("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_edit(
    request: Request,
    user_id: int,
    user: UserEdit,
    current_user=Depends(get_current_active_superuser),
):
    """
    Update existing user
    """
    return edit_user(request.state.db, user_id, user)


@r.delete("/users/{user_id}", response_model=User, response_model_exclude_none=True)
async def user_delete(
    request: Request,
    user_id: int,
    current_user=Depends(get_current_active_superuser),
):
    """
    Delete existing user
    """
    return delete_user(request.state.db, user_id)
