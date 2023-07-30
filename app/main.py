from typing import Optional

from fastapi import FastAPI, status, Response, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    publish: bool = True
    rating: Optional[int] = None


my_posts = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    my_posts.append(post)
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return {"post_id": post_id}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post, db: Session = Depends(get_db)):
    return {"details": "Updated the post"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
