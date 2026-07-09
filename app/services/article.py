from sqlalchemy.orm import Session
from app.repositories.article import ArticleRepository
from app.schemas.article import ArticleWithAuthorSchema, ArticleCreateSchema, ArticleResponseSchema, ArticleUpdateSchema
from app.repositories.user import UserRepository
from app.services.user import UserNotFound

class ArticleNotFound(Exception):
    """статья не найдена"""
    ...

class PermissionDenied(Exception):
    """нет прав на это действие"""
    pass

class ArticleService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.article_repository = ArticleRepository(db)
        self.user_repository = UserRepository(db)

    def create_article(self, article_data: ArticleCreateSchema) -> ArticleResponseSchema:
        if self.user_repository.get_by_id(user_id=article_data.author_id) is None:
            raise UserNotFound(f"User with id {article_data.author_id} not found")
        article_orm = self.article_repository.create(title=article_data.title, content=article_data.content, author_id=article_data.author_id)
        
        self.db.commit()
        return ArticleResponseSchema.model_validate(article_orm)

    def get_article_by_id(self, article_id: str) -> ArticleResponseSchema:
        article = self.article_repository.get_by_id(article_id=article_id)
        if article is None:
            raise ArticleNotFound("Article not found")
        return ArticleResponseSchema.model_validate(article)
    
    def get_all_articles(self, limit: int = 100, offset: int = 0) -> list[ArticleResponseSchema]:
        articles = self.article_repository.get_all(limit=limit, offset=offset)
        return [ArticleResponseSchema.model_validate(article) for article in articles]
    
    def update_article(self, article_id: str, update_data: ArticleUpdateSchema, current_user_id: str) -> ArticleResponseSchema:
        article = self.article_repository.get_by_id(article_id=article_id)
        if article is None:
            raise ArticleNotFound("Article not found")
        if article.author_id != current_user_id:
            raise PermissionDenied("You are not the author of this article")
        
        updated_article = self.article_repository.update(article=article, title=update_data.title, content=update_data.content)

        self.db.commit()
        return ArticleResponseSchema.model_validate(updated_article)
    
    def delete_article(self, article_id: str, current_user_id: str) -> None:
        article = self.article_repository.get_by_id(article_id=article_id)
        if article is None:
            raise ArticleNotFound("Article not found")
        if article.author_id != current_user_id:
            raise PermissionDenied("You are not the author of this article")
        self.article_repository.delete(article=article)
        self.db.commit()