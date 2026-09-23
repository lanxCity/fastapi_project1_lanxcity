from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/vote",
    tags= ["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    
    # NB: post should be shown if not exist normally but unregistered user should be redirected to login page.
    if not db.get(models.Post, vote.post_id) or not db.get(models.User, current_user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Not found post or user")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    found_vote = vote_query.first()
    
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} already vote on the post {vote.post_id}")
        
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        
        db.add(new_vote)
        db.commit()
        return {"message": "post liked!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {vote.post_id} not found")
        
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "post unliked!"}
        
        
        
        
        
    
    