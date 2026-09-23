from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=["Users"]
    )

@router.get('/', response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    print(bool(users))
    
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='No user')
        
    return users

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser,
                db: Session = Depends(get_db)):
    
    mail_query = db.query(models.User).filter(models.User.email == user.email)
    
    if mail_query.first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='email already exist')
    

    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(models.User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                             detail=f"user id {id} does not exist")
    return user

@router.put('/{id}', response_model=schemas.User)
def update_user(id: int, updated_user: schemas.UpdateUser, 
                db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    if current_user.id != id:   
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not authenticated')
    
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user does not exist')
    
    
    user_query.update(updated_user.model_dump(), synchronize_session=False)
    db.commit()
    return user_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db)):

    user = db.get(models.User, id)
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user does not exist')
    
    if current_user.id != id:   
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User not authorized')
    
    db.delete(user)
    db.commit()
    return