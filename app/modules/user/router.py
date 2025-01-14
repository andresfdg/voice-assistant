from typing import List

from fastapi import APIRouter

from app.modules.user.schemas import User, UserCreate
from app.modules.user.services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[User])
async def get_users():
    users = await UserService.get_all_users()
    return users


@router.post("/", response_model=User)
async def create_user(user: UserCreate):
    new_user = await UserService.create_user(user.name, user.email, user.password)
    return new_user


@router.get("/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    user = await UserService.get_user_by_id(user_id)
    return user


# @router.put("/users/{user_id}", response_model=User)
# async def update_user(user_id: int, user: UserUpdate):
#     updated_user = await UserService.update_user(user_id, user.name, user.age)
#     return updated_user


# @router.delete("/users/{user_id}")
# async def delete_user(user_id: int):
#     result = await UserService.delete_user(user_id)
#     return result
