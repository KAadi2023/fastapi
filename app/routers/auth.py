from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlmodel import select
from typing import Annotated
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import SessionDep

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.Token)
def login(user_creds: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep):
    statement = select(models.User).where(models.User.email == user_creds.username)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.password_hash.verify(user_creds.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}