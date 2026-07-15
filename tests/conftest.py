from urllib.parse import quote_plus

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine

from app import models
from app.config import settings
from app.database import get_session
from app.main import app
from app.oauth2 import create_access_token


# -------------------------------------------------------------------
# Test database configuration
# -------------------------------------------------------------------

safe_password = quote_plus(settings.database_password)

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.database_user}:"
    f"{safe_password}@"
    f"{settings.database_host}:"
    f"{settings.database_port}/"
    f"{settings.database_name}_test"
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"options": "-c timezone=utc"},
)

SQLModel.metadata.create_all(engine)


# -------------------------------------------------------------------
# Database session
# -------------------------------------------------------------------

@pytest.fixture
def session():
    # Clean the database before each test.
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                TRUNCATE TABLE votes, posts, users
                RESTART IDENTITY CASCADE
                """
            )
        )

    with Session(engine) as session:
        yield session


# -------------------------------------------------------------------
# Test client
# -------------------------------------------------------------------

@pytest.fixture
def client(session: Session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    with TestClient(app) as test_client:
        yield test_client

    # Prevent this override from leaking into other test modules.
    app.dependency_overrides.clear()


# -------------------------------------------------------------------
# User fixtures
# -------------------------------------------------------------------

@pytest.fixture
def test_user(client: TestClient):
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201, response.text

    new_user = response.json()["data"]
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def test_user2(client: TestClient):
    user_data = {
        "email": "john@gmail.com",
        "password": "testpassword",
    }

    response = client.post("/users", json=user_data)

    assert response.status_code == 201, response.text

    new_user = response.json()["data"]
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token(
        {"user_id": test_user["id"]}
    )


@pytest.fixture
def authorized_client(
    client: TestClient,
    token: str,
):
    client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return client


# -------------------------------------------------------------------
# Post fixtures
# -------------------------------------------------------------------

@pytest.fixture
def test_posts(
    test_user,
    session: Session,
    test_user2
):
    posts = [
        models.Post(
            title="First Title",
            content="Content of first title",
            owner_id=test_user["id"],
        ),
        models.Post(
            title="Second Title",
            content="Content of second title",
            owner_id=test_user["id"],
        ),
        models.Post(
            title="Third Title",
            content="Content of third title",
            owner_id=test_user["id"],
        ),
        models.Post(
            title="Fourth Title",
            content="Content of fourth title",
            owner_id=test_user2["id"],
        ),
    ]

    session.add_all(posts)
    session.commit()

    for post in posts:
        session.refresh(post)

    return posts