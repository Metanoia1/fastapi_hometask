import aiohttp

from typing import Any, List, Dict

from .models import CreateUserParams, User


class UserRepository:
    def __init__(self):
        self._users: List[User] = []
        self._serial = len(self._users)

    async def create_user(self, user: CreateUserParams) -> User:
        user = User(id=self._serial, **user.dict())
        self._serial += 1
        self._users.append(user)
        return user

    async def list_users(self) -> List[User]:
        return self._users.copy()


class JSONPlaceholderUserRepository(UserRepository):
    def __init__(self):
        self._endpoint = "https://jsonplaceholder.typicode.com/users"

    async def _create_user(self, user: CreateUserParams) -> Dict[str, Any]:
        # Найдите способ не создавать эту сессию каждый раз в каждой функции
        # А создать одну на все время работы JSONPlaceholderUserRepository
        async with aiohttp.ClientSession() as session:
            resp = await session.post(self._endpoint, json=user.dict())
            raw_user = await resp.json()
            return raw_user

    async def _list_users(self) -> List[Dict[str, Any]]:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self._endpoint)
            raw_users = await resp.json()
            return raw_users

    def _convert_user(self, raw_user: Dict[str, Any]) -> User:
        return User(**raw_user)

    async def create_user(self, user: CreateUserParams) -> User:
        raw_user = await self._create_user(user)
        return self._convert_user(raw_user)

    async def list_users(self) -> List[User]:
        raw_users = await self._list_users()
        return [self._convert_user(raw_user) for raw_user in raw_users]


class UserRepositoryFactory:
    def __init__(self):
        self._repo = None

    def __call__(self) -> UserRepository:
        if self._repo is None:
            self._repo = JSONPlaceholderUserRepository()
        return self._repo


get_user_repository = UserRepositoryFactory()
