from typing import List

from fastapi import status, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schema, models, database, utils

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(database.get_db)):
    new_user = models.User(**user.model_dump())
    hashed_password = utils.get_hashed_password(user.password)
    user.password = hashed_password
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/", response_model=List[schema.UserOut])
def get_users(db: Session = Depends(database.get_db)):
    return db.query(models.User).all()
