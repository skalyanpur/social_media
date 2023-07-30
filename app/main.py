from typing import Optional

from fastapi import FastAPI, status, Response
from pydantic import BaseModel

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
def get_posts():
    return my_posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    my_posts.append(post)
    return {"data": post}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    return {"post_id": post_id}


@app.put("/posts/{post_id}")
def update_post(post_id: int, post: Post):
    return {"details": "Updated the post"}


@app.delete("/posts/{post_id}")
def delete_post(post_id: int):
    return Response(status_code=status.HTTP_204_NO_CONTENT)
