from .. import schemas, models, oauth2
from ..database import get_db
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, desc


router = APIRouter(
    prefix= '/posts',
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.PostRes])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
      
    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    for u in posts:
        u[0].votes = u[1]
    posts = [u[0] for u in posts]
    return posts


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')) \
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True) \
        .group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id: {post_id} not found!")
    post[0].votes = post[1]
    post = post[0]
    
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail=f"You are not authorized to view this post!")
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRes)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id: {post_id} does not exist!")    
    if post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"You are not authorized to delete this post!")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.PostRes)
def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post id: {post_id} does not exist!")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                        detail=f"You are not authorized to update this post!")
        
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()