from typing import List

from fastapi import APIRouter, Depends

from .dependencies import PostRepository, get_post_repository
from .models import (
    CreatePostParams,
    UpdatePostParams,
    Post,
    CreatedPost,
    DetailPost,
    UpdatedPost,
)


router = APIRouter()


@router.get("/", tags=["posts"], response_model=List[Post])
async def list_posts(
    repository: PostRepository = Depends(get_post_repository),
):
    posts = await repository.list_posts()
    return posts


@router.post("/", tags=["posts"], response_model=CreatedPost, status_code=201)
async def create_post(
    post: CreatePostParams,
    repository: PostRepository = Depends(get_post_repository),
):
    post = await repository.create_post(post)
    return post


@router.get("/{post_id}", tags=["posts"], response_model=DetailPost)
async def post_details(
    post_id: int,
    repository: PostRepository = Depends(get_post_repository),
):
    posts = await repository.post_details(post_id)
    return posts


@router.put("/{post_id}", tags=["posts"], response_model=UpdatedPost)
async def update_post(
    post_id: int,
    post: UpdatePostParams,
    repository: PostRepository = Depends(get_post_repository),
):
    post = await repository.update_post(post_id, post)
    return post
