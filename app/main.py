from typing import List

from fastapi import FastAPI, status, Response, Depends
from sqlalchemy.orm import Session

from . import models, schema
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

my_posts = []


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schema.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_post(post: schema.PostBase, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{post_id}", response_model=schema.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    return post


@app.put("/posts/{post_id}", response_model=schema.Post)
def update_post(post_id: int, post: schema.PostBase, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post_query.update(**post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
