from typing import Optional

from sqlmodel import Field, SQLModel

__all__ = (
    "Post",
    "PostCreate",
    "PostUpdate",
)


class Post(SQLModel, table=True):
    """This is the model connected to the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    complete: bool = True


class PostCreate(SQLModel, table=False):
    """This is the model, used mainly for serialization of inputs on create."""

    title: str
    complete: bool = True


class PostUpdate(PostCreate):
    """This is the model, used mainly for serialization of inputs on update."""
