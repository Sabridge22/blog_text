from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import UserORM


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: str) -> UserORM | None:
        return self.db.get(UserORM, user_id)
    
    def get_by_username(self, username: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.username == username)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_by_email(self, email: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def create(self, username: str, email: str, bio: str | None = None) -> UserORM:
        new_user = UserORM(username=username, email=email, bio=bio)
        self.db.add(new_user)
        return new_user
    
    def update(self, user: UserORM, username: str | None = None, bio: str | None = None) -> UserORM:
        if username is not None:
            user.username = username
        if bio is not None:
            user.bio = bio

        return user
    
    def delete(self, user: UserORM) -> None:
        self.db.delete(user)