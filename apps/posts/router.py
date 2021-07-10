from typing import List, Any, Dict

from fastapi import APIRouter, Depends

from .dependencies import PostRepository, get_post_repository
from .models import CreatePostParams, Post, UpdatePostParams, UpdatedPost


router = APIRouter()


@router.get("/{post_id}", tags=["posts"], response_model=Dict[str, Any])
async def list_posts(
    post_id,
    repository: PostRepository = Depends(get_post_repository),
):
    posts = await repository.post_detail(post_id)
    return posts


@router.get("/", tags=["posts"], response_model=List[Post])
async def list_posts(
    repository: PostRepository = Depends(get_post_repository),
):
    posts = await repository.list_posts()
    return posts


@router.post(
    "/", tags=["posts"], response_model=CreatePostParams, status_code=201
)
async def create_post(
    post: CreatePostParams,
    repository: PostRepository = Depends(get_post_repository),
):
    post = await repository.create_post(post)
    return post


@router.put(
    "/{post_id}", tags=["posts"], response_model=UpdatedPost, status_code=200
)
async def update_post(
    post_id,
    post: UpdatePostParams,
    repository: PostRepository = Depends(get_post_repository),
):
    post = await repository.update_post(post_id, post)
    return post
