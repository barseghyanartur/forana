import random
import unittest

from fake import FAKER
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from api import app  # noqa
from db import get_db  # noqa
from factories import GENRES
from models import Movie  # noqa

__all__ = ("ApiTestCase",)

# Database connection config
TEST_DATABASE_URL = "sqlite:///./test_test.db"
TEST_ENGINE = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)


# Override the get_db dependency to use the test database
def override_get_db():
    db = None
    try:
        db = SessionLocalTest()
        yield db
    finally:
        if db:
            db.close()


# Apply the patch for tests
app.dependency_overrides[get_db] = override_get_db


class ApiTestCase(unittest.TestCase):
    """API test cases."""

    def setUp(self):
        """Set up test environment. Runs before each test."""
        self.client = TestClient(app)
        SQLModel.metadata.create_all(TEST_ENGINE)

    def tearDown(self):
        """Tear down test environment. Runs after each test."""
        SQLModel.metadata.drop_all(TEST_ENGINE)

    def test_post(self) -> None:
        """Test HTTP POST method."""
        response = self.client.post(
            "/api/movie",
            json={
                "title": FAKER.sentence(),
                "year": FAKER.pyint(min_value=1900, max_value=2024),
                "runtime": FAKER.pyint(min_value=15, max_value=360),
                "genres": random.sample(GENRES, 5),
                "directors": [FAKER.name() for _ in range(2)],
                "actors": [FAKER.name() for _ in range(5)],
                "plot": FAKER.text(),
                "poster_url": FAKER.image_url(),
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self) -> None:
        """Test HTTP GET method (retrieve a single record option)."""
        data = {
            "title": FAKER.sentence(),
            "year": FAKER.pyint(min_value=1900, max_value=2024),
            "runtime": FAKER.pyint(min_value=15, max_value=360),
            "genres": random.sample(GENRES, 5),
            "directors": [FAKER.name() for _ in range(2)],
            "actors": [FAKER.name() for _ in range(5)],
            "plot": FAKER.text(),
            "poster_url": FAKER.image_url(),
        }
        movie = Movie(**data)
        with Session(TEST_ENGINE) as session:
            session.add(movie)
            session.commit()
            session.refresh(movie)

        response = self.client.get(f"/api/movie/{movie.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(movie.title, data["title"])

    def test_get_all(self) -> None:
        """Test HTTP GET method (retrieve all records option)."""
        data = {
            "title": FAKER.sentence(),
            "year": FAKER.pyint(min_value=1900, max_value=2024),
            "runtime": FAKER.pyint(min_value=15, max_value=360),
            "genres": random.sample(GENRES, 5),
            "directors": [FAKER.name() for _ in range(2)],
            "actors": [FAKER.name() for _ in range(5)],
            "plot": FAKER.text(),
            "poster_url": FAKER.image_url(),
        }
        movie = Movie(**data)
        with Session(TEST_ENGINE) as session:
            session.add(movie)
            session.commit()
            session.refresh(movie)

        response = self.client.get("/api/movie")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["title"], data["title"])

    def test_delete(self) -> None:
        """Test HTTP DELETE method."""
        data = {
            "title": FAKER.sentence(),
            "year": FAKER.pyint(min_value=1900, max_value=2024),
            "runtime": FAKER.pyint(min_value=15, max_value=360),
            "genres": random.sample(GENRES, 5),
            "directors": [FAKER.name() for _ in range(2)],
            "actors": [FAKER.name() for _ in range(5)],
            "plot": FAKER.text(),
            "poster_url": FAKER.image_url(),
        }
        movie = Movie(**data)
        with Session(TEST_ENGINE) as session:
            session.add(movie)
            session.commit()
            session.refresh(movie)

        response = self.client.delete(f"/api/movie/{movie.id}")
        self.assertEqual(response.status_code, 200)

        with Session(TEST_ENGINE) as session:
            deleted_movie = session.get(Movie, movie.id)
            self.assertIsNone(deleted_movie)

    def test_update(self) -> None:
        """Test HTTP PUT method."""
        data = {
            "title": FAKER.sentence(),
            "year": FAKER.pyint(min_value=1900, max_value=2024),
            "runtime": FAKER.pyint(min_value=15, max_value=360),
            "genres": random.sample(GENRES, 5),
            "directors": [FAKER.name() for _ in range(2)],
            "actors": [FAKER.name() for _ in range(5)],
            "plot": FAKER.text(),
            "poster_url": FAKER.image_url(),
        }
        movie = Movie(**data)
        with Session(TEST_ENGINE) as session:
            session.add(movie)
            session.commit()
            session.refresh(movie)

        new_data = {
            "title": FAKER.sentence(),
            "year": FAKER.pyint(min_value=1900, max_value=2024),
            "runtime": FAKER.pyint(min_value=15, max_value=360),
            "genres": random.sample(GENRES, 5),
            "directors": [FAKER.name() for _ in range(2)],
            "actors": [FAKER.name() for _ in range(5)],
            "plot": FAKER.text(),
            "poster_url": FAKER.image_url(),
        }
        response = self.client.put(
            f"/api/movie/{movie.id}",
            json=new_data,
        )
        self.assertEqual(response.status_code, 200)

        with Session(TEST_ENGINE) as session:
            updated_movie = session.get(Movie, movie.id)
            self.assertEqual(updated_movie.title, new_data["title"])
