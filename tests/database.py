from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy import text
from urllib.parse import quote_plus
from app.config import settings
from app.database import get_session
import pytest

### 1st way to connect db and create instances
user=settings.database_user
password=settings.database_password
host=settings.database_host
port=settings.database_port
database=settings.database_name

safe_password = quote_plus(password)

DATABASE_URL = f"postgresql+psycopg2://{user}:{safe_password}@{host}:{port}/{database}_test"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"options": "-c timezone=utc"})
SQLModel.metadata.create_all(engine)

def get_session_override():
    with Session(engine) as session:
        yield session

app.dependency_overrides[get_session] = get_session_override 

@pytest.fixture
def client():
    with engine.begin() as connection:
        connection.execute(text("TRUNCATE TABLE votes, posts, users RESTART IDENTITY CASCADE"))
    with TestClient(app) as test_client:
        yield test_client
