from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=50,
        )
    email: EmailStr
    bio: str | None = None

class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    bio: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    username: str | None = Field(None, min_length=3, max_length=50)
    bio: str | None = None