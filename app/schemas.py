from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from .database import Base


# Pydantic schema
# Request body validation and serialization

# ===============> Users 
# = users request
class UserBase(BaseModel):
    name: str
    username: str = 'user'
    # is_verified: bool = False
    # followers: Optional[int] = 0
    
    # replace config class
    model_config = {
            "from_attributes": True
        }

class CreateUser(UserBase):
    email: EmailStr
    age: int
    password: str
    
class UpdateUser(UserBase):
    pass

# = user response
class User(UserBase):
    email: EmailStr
    id: int
    
    # class Config:
    #     orm_mode = True
    
    

# ==============> posts
# = posts request
class PostBase(BaseModel):
    title: str
    content: str
    
    model_config = {
        "from_attributes": True
    }

class CreatePost(PostBase):
    pass

class UpdatePost(PostBase):
    pass

# = post response
class Post(PostBase):
    id: int
    owner_id: int
    owner: User

# ==============> login request/validation
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# === access token schema
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

# ==================> Vote for post
class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]
    
    model_config = {
           "from_attributes": True
       }
    

# ===================> trying out
class PostOut(BaseModel):
    post: Post
    votes: int
    
    model_config = {
            "from_attributes": True
        }
