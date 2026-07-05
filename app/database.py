from sqlmodel import create_engine, Session
from typing import Annotated
from fastapi import Depends
from urllib.parse import quote_plus
from psycopg2.extras import RealDictCursor
import psycopg2
import time
from .config import settings

#### 1st way to connect db and create instances
user=settings.database_user
password=settings.database_password
host=settings.database_host
port=settings.database_port
database=settings.database_name

safe_password = quote_plus(password)

DATABASE_URL = f"postgresql+psycopg2://{user}:{safe_password}@{host}:{port}/{database}"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"options": "-c timezone=utc"})

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

#### 2nd way to connect db and create instances to execute query
# while True:
#     try:
#         conn = psycopg2.connect(
#             host=settings.database_host,
#             database=settings.database_name,
#             user=settings.database_user,
#             password=settings.database_password,
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as e:
#         print(f"Database connection failed: {e}")
#         time.sleep(2)
