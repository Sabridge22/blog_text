from sqlalchemy import ForeignKey, String, DateTime, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from datetime import datetime

class ArticleORM(Base):
    __tablename__ = "articles"

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    