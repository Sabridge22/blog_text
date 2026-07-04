from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema


class UserNotFound(Exception):
    """Пользователь не найден"""
    ...

class UserAlreadyExists(Exception):
    """Пользователь уже существует"""
    ...


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)
    
    def register_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        if self.user_repository.get_by_username(user_data.username) is not None:
            raise UserAlreadyExists("Username already taken")
        if self.user_repository.get_by_email(user_data.email) is not None:
            raise UserAlreadyExists("Email already taken")
        new_user = self.user_repository.create(user_data.username, user_data.email, user_data.bio)
        self.db.commit()
        return UserResponseSchema.model_validate(new_user)
        
    def get_user_by_id(self, user_id: str) -> UserResponseSchema:
        user = self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFound("User not found")
        return UserResponseSchema.model_validate(user)
    
    def update_user(self, user_id: str, update_data: UserUpdateSchema) -> UserResponseSchema:
        user = self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFound("User not found")
        if update_data.username is not None:
            existing = self.user_repository.get_by_username(update_data.username)
            if existing and existing.id != user_id:
                raise UserAlreadyExists("Username already taken")
        self.user_repository.update(user=user, username=update_data.username, bio=update_data.bio)
        self.db.commit()
        return UserResponseSchema.model_validate(user)
    
    def delete_user(self, user_id: str) -> None:
        user = self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFound("User not found")
        self.user_repository.delete(user=user)
        self.db.commit()