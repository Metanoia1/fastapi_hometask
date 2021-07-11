from pydantic import BaseModel, EmailStr


class CreateUserParams(BaseModel):
    name: str
    username: str
    email: EmailStr
    phone: str


class User(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    phone: str
