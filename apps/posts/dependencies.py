import aiohttp

from typing import Any, List, Dict
from .models import (
    CreatePostParams,
    Post,
    PostDetail,
    UpdatePostParams,
    UpdatedPost,
)


class PostRepository:
    def __init__(self):
        self._posts: List[Post] = []
        self._serial = len(self._posts)

    async def create_post(self, post: CreatePostParams) -> Post:
        post = Post(id=self._serial, **post.dict())
        self._serial += 1
        self._posts.append(post)
        return post

    async def list_posts(self) -> List[Post]:
        return self._posts.copy()


class JSONPlaceholderPostRepository(PostRepository):
    def __init__(self, session):
        self._endpoint = "https://jsonplaceholder.typicode.com/posts"
        self._users_endpoint = "https://jsonplaceholder.typicode.com/users"
        self._comments_endpoint = (
            "https://jsonplaceholder.typicode.com/comments"
        )
        self.session = session

    async def _update_post(
        self, post_id, post: UpdatePostParams
    ) -> UpdatePostParams:
        async with self.session() as session:
            resp = await session.put(
                f"{self._endpoint}/{post_id}", json=post.dict()
            )
            raw_post = await resp.json()
            return raw_post

    async def _create_post(self, post: CreatePostParams) -> Dict[str, Any]:
        async with self.session() as session:
            resp = await session.post(self._endpoint, json=post.dict())
            raw_post = await resp.json()
            return raw_post

    async def _list_posts(self) -> List[Dict[str, Any]]:
        async with self.session() as session:
            resp = await session.get(self._endpoint)
            raw_posts = await resp.json()
            return raw_posts

    async def _get_users(self) -> List[Dict[str, Any]]:
        async with self.session() as session:
            resp = await session.get(self._users_endpoint)
            raw_users = await resp.json()
            return raw_users

    async def _get_comments(self, post_id) -> List[Dict[str, Any]]:
        async with self.session() as session:
            resp = await session.get(
                f"{self._comments_endpoint}?postId={post_id}"
            )
            comments = await resp.json()
            comments_list = []
            for comment in comments:
                add = {
                    "id": comment["id"],
                    "body": comment["body"],
                }
                comments_list.append(add)
            return comments_list

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)

    def _convert_post_create(self, raw_post: Dict[str, Any]) -> Post:
        return CreatePostParams(**raw_post)

    def _convert_post_update(self, raw_post: Dict[str, Any]) -> UpdatedPost:
        return UpdatedPost(**raw_post)

    def _convert_post_datails(self, raw_post: Dict[str, Any]) -> Post:
        return PostDetail(**raw_post)

    async def create_post(self, post: CreatePostParams) -> Post:
        raw_post = await self._create_post(post)
        return self._convert_post_create(raw_post)

    async def update_post(
        self, post_id, post: UpdatePostParams
    ) -> UpdatedPost:
        raw_post = await self._update_post(post_id, post)
        return self._convert_post_update(raw_post)

    async def _merge_post_with_author(self, raw_post, raw_users):
        for user in raw_users:
            if user["id"] == raw_post["userId"]:
                try:
                    author = {
                        "id": user["id"],
                        "name": user["name"],
                        "email": user["email"],
                    }
                except KeyError:
                    author = {"error": "KeyError"}
                raw_post["author"] = author

    async def _merge_posts_with_author(self, raw_posts, raw_users):
        for post in raw_posts:
            for user in raw_users:
                if user["id"] == post["userId"]:
                    try:
                        author = {
                            "id": user["id"],
                            "name": user["name"],
                            "email": user["email"],
                        }
                    except KeyError:
                        author = {"error": "KeyError"}
                    post["author"] = author

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        raw_users = await self._get_users()
        await self._merge_posts_with_author(raw_posts, raw_users)
        return [self._convert_post(raw_post) for raw_post in raw_posts]

    async def post_detail(self, post_id):
        async with self.session() as session:
            resp = await session.get(f"{self._endpoint}/{post_id}")
            raw_post = await resp.json()
            comments = await self._get_comments(post_id)
            users = await self._get_users()
            await self._merge_post_with_author(raw_post, users)
            raw_post["comments"] = comments
            return self._convert_post_datails(raw_post)


class PostRepositoryFactory:
    def __init__(self, session):
        self._repo = None
        self.session = session

    def __call__(self) -> PostRepository:
        if self._repo is None:
            self._repo = JSONPlaceholderPostRepository(self.session)
        return self._repo


get_post_repository = PostRepositoryFactory(aiohttp.ClientSession)
