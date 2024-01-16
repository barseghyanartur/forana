import random
from copy import deepcopy
from fake import FACTORY, FAKER, SQLAlchemyModelFactory, PreSave

from db import SESSION, SessionLocal
from models import Movie


GENRES = (
    "Action",
    "Adventure",
    "Animation",
    "Biography",
    "Comedy",
    "Crime",
    "Drama",
    "Family",
    "Fantasy",
    "Film-Noir",
    "History",
    "Horror",
    "Music",
    "Musical",
    "Mystery",
    "Romance",
    "Sci-Fi",
    "Sport",
    "Thriller",
    "War",
    "Western",
)


def pick_genres(movie: Movie, nb: int = 1) -> None:
    """Helper function for genres."""
    movie.genres = random.sample(GENRES, nb)


def pick_actors(movie: Movie, nb: int = 1) -> None:
    """Helper function for actors."""
    movie.actors = [FAKER.name() for _ in range(nb)]


def get_session():
    return SessionLocal()


class MovieFactory(SQLAlchemyModelFactory):
    """Movie factory."""

    title = FACTORY.sentence()
    year = FACTORY.pyint(min_value=1900, max_value=2024)
    runtime = FACTORY.pyint(min_value=15, max_value=360)
    genres = PreSave(pick_genres, nb=2)
    director = FACTORY.name()
    actors = PreSave(pick_actors, nb=5)
    plot = FACTORY.text()
    poster_url = FACTORY.image_url()

    class Meta:
        model = Movie
        get_or_create = ("title",)

    class MetaSQLAlchemy:
        get_session = get_session


if __name__ == "__main__":
    MovieFactory.create_batch(100)
