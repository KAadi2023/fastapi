from fastapi import APIRouter, Depends, HTTPException, Response, status, Query
from .. import models, schemas, oauth2
from ..database import SessionDep
from sqlmodel import func, select

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

### Using direct SQL queries with psycopg2
# @router.get("/")
# async def get_posts():
#     cursor.execute("SELECT * FROM posts")
#     posts = cursor.fetchall()
#     return {"message": "All Posts retrieved successfully", "data": posts}


### Using SQLModel with SQLAlchemy ORM  
@router.get("", response_model=schemas.PostListResponse)
def get_posts(
    session: SessionDep,
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = Query(default=10, ge=1, le=100),
    skip: int = Query(default=0, ge=0),
    search: str | None = Query(default=None)
):
    statement = (
        select(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )
    if search:
        statement = statement.where(models.Post.title.ilike(f"%{search}%"))

    statement = (
        statement
        .order_by(models.Post.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    results = session.exec(statement).all()

    posts = [
        {
            "post": post,
            "votes": votes
        }
        for post, votes in results
    ]

    return {
        "message": "All Posts retrieved successfully",
        "data": posts
    }


### Using SQLModel with SQLAlchemy ORM
@router.get("/latest", response_model=schemas.PostCreateResponse)
async def get_latest_post(session: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    statement = select(models.Post).order_by(models.Post.created_at.desc()).limit(1)
    latest_post = session.exec(statement).first()
    if not latest_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    return {"message": "Latest Post retrieved successfully", "data": latest_post}


### Using direct SQL queries with psycopg2
# @router.get("/{id}")
# async def get_post(id: int):
#     cursor.execute("SELECT * FROM posts WHERE id = %s", (str(id),))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         # return {"message": "Post not found"}
#     return {"message": "Post retrieved successfully", "data": post}


### Using SQLModel with SQLAlchemy ORM
@router.get("/{id}", response_model=schemas.PostWithVotes)
async def get_post(id: int, session: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    statement = (
        
        select(
            models.Post,
            func.count(models.Vote.post_id).label("votes")
        )
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .where(models.Post.id == id)
        .group_by(models.Post.id)
    )
    result = session.exec(statement).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    post, votes = result
    return {"post": post, "votes": votes}

### Using direct SQL queries with psycopg2
# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_post(reqBody: schemas.PostCreate):
#     print(f"Creating post with title: {reqBody.title}")
#     new_post =  cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *", 
#                    (reqBody.title, reqBody.content, reqBody.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {"message": "Post created successfully", "data": new_post}


### Using SQLModel with SQLAlchemy ORM
@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateResponse)
async def create_post(reqBody: schemas.PostCreate, session: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    new_post = models.Post(title=reqBody.title, content=reqBody.content, published=reqBody.published, owner_id=current_user.id)
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return {"message": "Post created successfully", "data": new_post}


### Using direct SQL queries with psycopg2    
# @router.put("/{id}")
# async def update_post(id: int, reqBody: schemas.PostCreate, response: Response):
#     cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *", (reqBody.title, reqBody.content, reqBody.published, str(id)))
#     post = cursor.fetchone()
#     conn.commit()
#     if not post:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         return {"message": "Post not found"}
#     return {"message": "Post updated successfully", "data": post}


### Using SQLModel with SQLAlchemy ORM
@router.put("/{id}", response_model=schemas.PostCreateResponse)
async def update_post(id: int, reqBody: schemas.PostCreate, session: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    statement = select(models.Post).where(models.Post.id == id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if(post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    post.title = reqBody.title
    post.content = reqBody.content
    post.published = reqBody.published
    
    session.add(post)
    session.commit()
    session.refresh(post)
    
    return {"message": "Post updated successfully", "data": post}


### Using direct SQL queries with psycopg2
# @router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(id: int):
#     cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *", (str(id),))
#     post = cursor.fetchone()
#     conn.commit()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
#     # return {"message": "Post deleted successfully"}


### Using SQLModel with SQLAlchemy ORM
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, session: SessionDep, current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    statement = select(models.Post).where(models.Post.id == id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    if(post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    session.delete(post)
    session.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    # return {"message": "Post deleted successfully"}

