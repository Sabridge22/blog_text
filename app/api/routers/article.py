from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from app.schemas.article import ArticleCreateSchema, ArticleResponseSchema, ArticleUpdateSchema
from app.services.article import ArticleNotFound, ArticleService, PermissionDenied
from app.db.session import get_db
from typing import Annotated

from app.services.user import UserNotFound

router = APIRouter(prefix='/articles')

@router.post('/', response_model=ArticleResponseSchema, status_code=status.HTTP_201_CREATED)
def create_article(article_data: ArticleCreateSchema, db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.create_article(article_data=article_data)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.get('/', response_model=list[ArticleResponseSchema], status_code=status.HTTP_200_OK)
def get_articles(limit: int = 100, offset: int = 0, db: Session = Depends(get_db)):
    service = ArticleService(db)
    return service.get_all_articles(limit=limit, offset=offset)

@router.get('/{article_id}', response_model=ArticleResponseSchema, status_code=status.HTTP_200_OK)
def get_article_by_id(article_id: Annotated[str, Path], db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.get_article_by_id(article_id=article_id)
    except ArticleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.put('/{article_id}', response_model=ArticleResponseSchema, status_code=status.HTTP_200_OK)
def update_article(article_id: Annotated[str, Path], update_data: ArticleUpdateSchema, current_user_id: str, db: Session = Depends(get_db)):
    service = ArticleService(db)
    try:
        return service.update_article(article_id=article_id, update_data=update_data, current_user_id=current_user_id)
    except ArticleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDenied as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
@router.delete('/{article_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: Annotated[str, Path], current_user_id: str, db: Session = Depends(get_db)) -> None:
    service = ArticleService(db)
    try:
        service.delete_article(article_id=article_id, current_user_id=current_user_id)
    except PermissionDenied as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    except ArticleNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    