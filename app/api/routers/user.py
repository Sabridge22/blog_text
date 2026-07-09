from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm import Session

from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from app.services.user import UserNotFound, UserAlreadyExists, UserService

from app.db.session import get_db
from typing import Annotated

router = APIRouter(prefix='/users')

@router.post('', response_model=UserResponseSchema, status_code = status.HTTP_201_CREATED)
def create_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.register_user(user_data=user_data)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: Annotated[str, Path], db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_id(user_id=user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
@router.put('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def update_user(user_id: Annotated[str, Path], update_data: Annotated[UserUpdateSchema, Body], db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.update_user(user_id=user_id, update_data=update_data)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete('/{user_id}')
def delete_user(user_id: Annotated[str, Path], db: Session = Depends(get_db)) -> None:
    service = UserService(db)
    try:
        service.delete_user(user_id=user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = str(e))
