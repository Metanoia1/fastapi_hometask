from typing import Any, List, Dict

from fastapi import Depends

from aiohttp import ClientSession

from apps.session import get_session
from .models import CreateUserParams, User


class UserRepository:
    def __init__(self, session):
        self._session = session
        self._endpoint = "https://jsonplaceholder.typicode.com/users"

    async def list_users(self) -> List[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]

    async def create_user(self, user: CreateUserParams):
        raw_user = await self._create_user(user)
        return self._convert_user(raw_user)

    async def _list_users(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._endpoint)
        raw_users = await resp.json()
        return raw_users

    async def _create_user(self, user: CreateUserParams) -> Dict[str, Any]:
        resp = await self._session.post(self._endpoint, json=user.dict())
        raw_user = await resp.json()
        return raw_user

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)


class UserRepositoryFactory:
    async def __call__(
        self, session: ClientSession = Depends(get_session)
    ) -> UserRepository:
        return UserRepository(session)


get_user_repository = UserRepositoryFactory()
