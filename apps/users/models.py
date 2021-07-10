from pydantic import BaseModel, EmailStr


class CreateUserParams(BaseModel):
    username: str
    email: EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
