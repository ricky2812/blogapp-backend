from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from typing import Optional
from datetime import datetime



class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass

class PostRes(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    votes: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id : Optional[int] = None



class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)
