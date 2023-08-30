from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
import database
import crud
import models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["root"])
async def root():
    return {"data": "Hello"}


# GET todos os users
@app.get("/users/", tags=["users"], response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.read_users(db=db, skip=skip, limit=limit)
    return users


# CREATE user
@app.post("/users/", tags=["users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.read_user_by_email(email=user.email, db=db)
    if new_user:
        raise HTTPException(status_code=400, detail="Email já em uso")
    return crud.create_user(db=db, user=user)
