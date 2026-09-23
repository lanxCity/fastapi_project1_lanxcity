from fastapi import Depends, status, HTTPException, APIRouter
# to get the login credentials instead of using "UserLogin" schema
from fastapi.security import OAuth2PasswordRequestForm  
from sqlalchemy.orm import Session
from .. import schemas, models, database, utils, oauth2

router = APIRouter(
    tags=['Authentication']
    )

@router.post('/login', response_model=schemas.Token)
def login(login_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    # NB: when OAuth2PasswordRequestForm is used, it only returns "username" and "password"
    # While testing, use "form_data" instead of "raw" to send credentials
    
    user = db.query(models.User).filter(models.User.email == login_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid credentials')
    
    if not utils.verify(login_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= 'Invalid credentials')
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}  