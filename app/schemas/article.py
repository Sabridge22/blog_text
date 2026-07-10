from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from .user import UserResponseSchema

class ArticleCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)
    author_id: str

class ArticleUpdateSchema(BaseModel):
    title: str | None = None
    content: str | None = None

class ArticleResponseSchema(BaseModel):
    id: str
    title: str
    content: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class ArticleWithAuthorSchema(ArticleResponseSchema):
    author: UserResponseSchema
    
