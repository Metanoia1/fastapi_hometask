from typing import List

from fastapi import APIRouter, Depends

from .dependencies import UserRepository, get_user_repository
from .models import CreateUserParams, User


router = APIRouter()


@router.get("/", tags=["users"], response_model=List[User])
async def list_users(
    repository: UserRepository = Depends(get_user_repository),
):
    users = await repository.list_users()
    return users


@router.post("/", tags=["users"], response_model=User, status_code=201)
async def create_user(
    user: CreateUserParams,
    repository: UserRepository = Depends(get_user_repository),
):
    user = await repository.create_user(user)
    return user
