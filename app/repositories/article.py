from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.article import ArticleORM


class ArticleRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, article_id: str) -> ArticleORM | None:
        return self.db.get(ArticleORM, article_id)