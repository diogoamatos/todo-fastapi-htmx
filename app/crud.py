from sqlalchemy.orm import Session

from . import models, schemas


# CREATE, READ, UPDATE, DELETE User get
# Get um unico usuario pelo seu id
def read_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


# GET todos os usuarios com um limite de 100
def read_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(100).all()


# GET um unico usuario por seu email
def read_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


# CREATE um usuario a partir do schema UserCreate e commita para o banco
def create_user(db: Session, user: schemas.UserCreate):
    fake_pwd = user.password + ":fakehashed"
    new_user = models.User(email=user.email, password=fake_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# CREATE, READ, UPDATE, DELETE ToDo
# GET todos os ToDos existentes de um usuario
def read_todos_by_user(db: Session, owner_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Todo)
        .filter(models.Todo.owner_id == owner_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


# GET todos os ToDos existentes com um limite de 100
def read_todos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Todo).offset(skip).limit(limit).all()


# CREATE um ToDo de um User
def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    new_todo = models.Todo(**dict(todo), owner_id=user_id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo
