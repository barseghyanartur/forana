import unittest

from fake import FAKER
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel, create_engine

from api import app  # noqa
from db import get_db  # noqa
from models import Item  # noqa

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
            "/api/item",
            json={
                "title": FAKER.sentence(),
                "published": FAKER.pybool(),
            },
        )
        self.assertEqual(response.status_code, 200)

    def test_get(self) -> None:
        """Test HTTP GET method (retrieve a single record option)."""
        data = {
            "title": FAKER.sentence(),
            "published": FAKER.pybool(),
        }
        item = Item(**data)
        with Session(TEST_ENGINE) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        response = self.client.get(f"/api/item/{item.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item.title, data["title"])

    def test_get_all(self) -> None:
        """Test HTTP GET method (retrieve all records option)."""
        data = {
            "title": FAKER.sentence(),
            "published": FAKER.pybool(),
        }
        item = Item(**data)
        with Session(TEST_ENGINE) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        response = self.client.get("/api/item")
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 1)
        self.assertEqual(response_data[0]["title"], data["title"])

    def test_delete(self) -> None:
        """Test HTTP DELETE method."""
        data = {
            "title": FAKER.sentence(),
            "published": FAKER.pybool(),
        }
        item = Item(**data)
        with Session(TEST_ENGINE) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        response = self.client.delete(f"/api/item/{item.id}")
        self.assertEqual(response.status_code, 200)

        with Session(TEST_ENGINE) as session:
            deleted_item = session.get(Item, item.id)
            self.assertIsNone(deleted_item)

    def test_update(self) -> None:
        """Test HTTP PUT method."""
        data = {
            "title": FAKER.sentence(),
            "published": FAKER.pybool(),
        }
        item = Item(**data)
        with Session(TEST_ENGINE) as session:
            session.add(item)
            session.commit()
            session.refresh(item)

        new_data = {
            "title": FAKER.sentence(),
            "published": FAKER.pybool(),
        }
        response = self.client.put(
            f"/api/item/{item.id}",
            json=new_data,
        )
        self.assertEqual(response.status_code, 200)

        with Session(TEST_ENGINE) as session:
            updated_post = session.get(Item, item.id)
            self.assertEqual(updated_post.title, new_data["title"])
