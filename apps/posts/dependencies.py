from typing import Any, List, Dict

from fastapi import Depends

from aiohttp import ClientSession

from apps.session import get_session
from .models import (
    CreatePostParams,
    Post,
    CreatedPost,
    DetailPost,
    UpdatePostParams,
    UpdatedPost,
)


class PostRepository:
    def __init__(self, session) -> None:
        self._session = session
        self._posts = "https://jsonplaceholder.typicode.com/posts"
        self._users = "https://jsonplaceholder.typicode.com/users"
        self._comments = "https://jsonplaceholder.typicode.com/comments"

    async def list_posts(self) -> List[Post]:
        raw_posts = await self._list_posts()
        raw_users = await self._get_users()
        posts = await self._merge_posts_with_author(raw_posts, raw_users)
        return [self._convert_post(post) for post in posts]

    async def create_post(self, post: CreatePostParams):
        raw_post = await self._create_post(post)
        return self._convert_created_post(raw_post)

    async def post_details(self, post_id: int) -> DetailPost:
        raw_post = await self._post_details(post_id)
        return self._convert_datail_post(raw_post)

    async def update_post(self, post_id: int, post: UpdatePostParams):
        raw_post = await self._update_post(post_id, post)
        return self._convert_updated_post(raw_post)

    async def _list_posts(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._posts)
        raw_posts = await resp.json()
        return raw_posts

    async def _create_post(self, post: CreatePostParams) -> Dict[str, Any]:
        resp = await self._session.post(self._posts, json=post.dict())
        raw_post = await resp.json()
        return raw_post

    async def _post_details(self, post_id: int) -> Dict[str, Any]:
        resp = await self._session.get(f"{self._posts}/{post_id}")
        raw_post = await resp.json()
        raw_comments = await self._get_comments(post_id)
        raw_users = await self._get_users()
        post = await self._merge_post_with_author(raw_post, raw_users)
        post["comments"] = raw_comments
        return post

    async def _update_post(
        self, post_id: int, post: UpdatePostParams
    ) -> Dict[str, Any]:
        resp = await self._session.put(
            f"{self._posts}/{post_id}", json=post.dict()
        )
        raw_post = await resp.json()
        return raw_post

    def _convert_post(self, raw_post: Dict[str, Any]) -> Post:
        return Post(**raw_post)

    def _convert_created_post(self, raw_post: Dict[str, Any]) -> CreatedPost:
        return CreatedPost(**raw_post)

    def _convert_datail_post(self, raw_post: Dict[str, Any]) -> DetailPost:
        return DetailPost(**raw_post)

    def _convert_updated_post(self, raw_post: Dict[str, Any]) -> UpdatedPost:
        return UpdatedPost(**raw_post)

    async def _get_users(self) -> List[Dict[str, Any]]:
        resp = await self._session.get(self._users)
        raw_users = await resp.json()
        return raw_users

    async def _get_comments(self, post_id: int) -> List[Dict[str, Any]]:
        resp = await self._session.get(f"{self._comments}?postId={post_id}")
        comments = await resp.json()
        comments_list = []
        for c in comments:
            comment = {
                "id": c["id"],
                "body": c["body"],
            }
            comments_list.append(comment)
        return comments_list

    async def _merge_post_with_author(
        self, raw_post: Dict[str, Any], raw_users: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        post = dict(raw_post)
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
                post["author"] = author
        return post

    async def _merge_posts_with_author(
        self, posts: List[Dict[str, Any]], users: List[Dict[str, Any]]
    ) -> List:
        posts = list(posts)
        for post in posts:
            for user in users:
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
        return posts


class PostRepositoryFactory:
    async def __call__(
        self, session: ClientSession = Depends(get_session)
    ) -> PostRepository:
        return PostRepository(session)


get_post_repository = PostRepositoryFactory()
