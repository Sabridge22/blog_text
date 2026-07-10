from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase

class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(primary_key=True, unique=True, default = lambda: str(uuid4()))