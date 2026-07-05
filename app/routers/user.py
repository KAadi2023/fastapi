from .. import models, schemas, utils
from ..database import SessionDep
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
async def create_user(reqBody: schemas.UserCreate, session: SessionDep):
    existing_user = session.exec(select(models.User).where(models.User.email == reqBody.email)).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {reqBody.email} already exists")
    
    hashed_password = utils.password_hash.hash(reqBody.password)
    reqBody.password = hashed_password
    new_user = models.User(email=reqBody.email, password=reqBody.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return {"message": "User created successfully", "data": new_user}


@router.get("/{id}", response_model=schemas.UserCreateResponse)
async def get_user(id: int, session: SessionDep):
    statement = select(models.User).where(models.User.id == id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return {"message": "User retrieved successfully", "data": user}