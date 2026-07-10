from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from app.schemas.article import ArticleCreateSchema, ArticleResponseSchema, ArticleUpdateSchema, ArticleWithAuthorSchema
from app.services.article import ArticleNotFound, ArticleService
from app.db.session import get_db
from typing import Annotated

from app.services.user import UserNotFound, UserAlreadyExists

router = APIRouter(prefix='/articles')

@router.post('/', response_model=ArticleResponseSchema, status_code=status.HTTP_201_CREATED)
def create_article(article_data: ArticleCreateSchema, db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.create_article(article_data=article_data)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))