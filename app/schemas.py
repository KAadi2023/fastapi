from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime
from typing import Optional

### ------------------------- User Schemas --------------------------------

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserCreateResponse(BaseModel):
    message: str
    data: User

class UserListResponse(BaseModel):
    message: str
    data: list[User]

class UserLogin(BaseModel):
    email: EmailStr
    password: str


### ------------------------- Auth Schema ------------------------------------

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


### ------------------------- Post Schemas --------------------------------
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner_id: int
    created_at: datetime
    owner: User

    model_config = ConfigDict(from_attributes=True)

class PostCreateResponse(BaseModel):
    message: str
    data: Post

class PostWithVotes(BaseModel):
    post: Post
    votes: int

class PostListResponse(BaseModel):
    message: str
    data: list[PostWithVotes]


### ------------------------- Vote Schemas --------------------------------
class Vote(BaseModel):
    post_id: int
    dir: int

