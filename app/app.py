import uvicorn

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import schemas
import database
import crud
import models

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", tags=["index"], response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# GET todos os users
@app.get("/users/", tags=["users"], response_model=list[schemas.User])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.read_users(db=db, skip=skip, limit=limit)
    return users


# GET user por id
@app.get("/users/{user_id}", tags=["users"], response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.read_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    db_user.items = crud.read_todos_by_user(db=db, owner_id=user_id)
    return db_user


# CREATE user
@app.post("/users/", tags=["users"], response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    new_user = crud.read_user_by_email(email=user.email, db=db)
    if new_user:
        raise HTTPException(status_code=400, detail="Email já em uso")
    return crud.create_user(db=db, user=user)


# GET todos os ToDos
@app.get("/todos/", tags=["todos"], response_model=list[schemas.Todo])
def get_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.read_todos(db=db, skip=skip, limit=limit)


# CREATE um ToDo
@app.post("/users/{user_id}/todos", tags=["todos"], response_model=schemas.Todo)
def create_todo_for_user(
    todo: schemas.TodoCreate, user_id: int, db: Session = Depends(get_db)
):
    user = crud.read_user(db=db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")
    return crud.create_todo(db=db, todo=todo, user_id=user_id)


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
