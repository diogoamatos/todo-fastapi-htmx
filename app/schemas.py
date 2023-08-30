from pydantic import BaseModel


# Schemas para ToDo
class TodoBase(BaseModel):
    title: str
    content: str | None = None


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


# Schemas para User
class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Todo] = []

    class Conig:
        orm_mode = True
