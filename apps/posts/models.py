from typing import Dict, Any, List

from pydantic import BaseModel


class CreatePostParams(BaseModel):
    author_id: int
    title: str
    body: str


class Post(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]


class CreatedPost(BaseModel):
    id: int
    author_id: int
    title: str
    body: str


class DetailPost(BaseModel):
    id: int
    title: str
    body: str
    author: Dict[str, Any]
    comments: List[Dict[str, Any]]


class UpdatePostParams(BaseModel):
    title: str
    body: str


class UpdatedPost(BaseModel):
    id: int
    title: str
    body: str
