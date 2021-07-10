from typing import Dict, Any, List

from pydantic import BaseModel, EmailStr


class CreatePostParams(BaseModel):
    author_id: int
    title: str
    body: str


class UpdatePostParams(BaseModel):
    title: str
    body: str


class UpdatedPost(BaseModel):
    id: int
    title: str
    body: str


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]


class PostDetail(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]
    comments: List[Dict]
