from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from ..models import Post
from .. import schemas, models, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
    )

# ===> posts endpoints
@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # posts = db.query(models.Post).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # posts = db.query(models.Post).filter(models.Post.title.ilike(f'%{search}%')).limit(limit).offset(skip).all()  # "ilike" for case insensitive
    
    # >>>>  of sql "join" with sqlalchemy orm
    # >>>> We wanna include the num of votes for each post in the response.
    # NB: sql uses "left outer join" by default while in sqlalchemy it inner
    
    posts = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.title.ilike(f'%{search}%')).limit(limit).offset(skip).all()
    
    
    if not posts:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail='No posts')
    
    return [
        {
        'post': post,
        'votes': votes
        }
        for post, votes in posts 
    ]
    
    
@router.post('/', response_model=schemas.PostOut, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.CreatePost,db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(**post.model_dump(), owner_id=current_user.id)
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return {"post": new_post, "votes": 0}

@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    # post = db.get(models.Post, id)
    
    post = db.query(
        models.Post, func.count(models.Vote.post_id).label("votes")
        ).join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    
    # since it is returning two objects inside tuple (Post, Votes)
    return {
        'post': post[0],
        'votes': post[1]
        }
    

@router.put('/{id}', response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform action')
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user id {id} does not exist')
        
    if post.owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Not authorized to perform action')
    
    db.delete(post)
    db.commit()
    return
    
