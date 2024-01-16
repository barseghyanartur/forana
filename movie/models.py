from typing import List, Optional

from sqlmodel import Column, Field, JSON, SQLModel

__all__ = (
    "Movie",
    "MovieCreate",
    "MovieUpdate",
)


class Movie(SQLModel, table=True):
    """This is the model connected to the database."""

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    year: int
    runtime: int
    genres: List[str] = Field(sa_column=Column(JSON))
    director: str
    actors: List[str] = Field(sa_column=Column(JSON))
    plot: str
    poster_url: str


class MovieCreate(SQLModel, table=False):
    """This is the model, used mainly for serialization of inputs on create."""

    title: str
    year: int
    runtime: int
    genres: List[str] = Field(sa_column=Column(JSON))
    director: str
    actors: List[str] = Field(sa_column=Column(JSON))
    plot: str
    poster_url: str


class MovieUpdate(MovieCreate):
    """This is the model, used mainly for serialization of inputs on update."""
