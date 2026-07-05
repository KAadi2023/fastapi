from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from .. import models, schemas, oauth2
from ..database import SessionDep
from sqlmodel import select

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, session: SessionDep, current_user: models.User = Depends(oauth2.get_current_user)):
    post = session.get(models.Post, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} not found")
    
    existing_vote = session.exec(
        select(models.Vote).where(
            models.Vote.post_id == vote.post_id,
            models.Vote.user_id == current_user.id
        )
    ).first()

    if vote.dir == 1:
        if existing_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        session.add(new_vote)
        session.commit()
        return {"message": "Vote added successfully"}
    else:
        if not existing_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist for user {current_user.id} on post {vote.post_id}")
        session.delete(existing_vote)
        session.commit()
        return {"message": "Vote removed successfully"}