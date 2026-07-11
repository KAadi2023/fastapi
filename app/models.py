from sqlmodel import Relationship, SQLModel, Field, String, text
from datetime import datetime
from sqlalchemy.dialects.postgresql import TIMESTAMP

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(sa_column_kwargs={"unique": True, "index": True, "nullable": False})
    password: str
    created_at: datetime | None = Field(
        default=None,
        sa_type=TIMESTAMP(timezone=True),
        sa_column_kwargs={"server_default": text("now()"), "nullable": False}
    )
    phone_number: str = Field(sa_type=String(), nullable=True, sa_column_kwargs={"unique": True, "index": True})


class Post(SQLModel, table=True):
    __tablename__ = "posts"

    id: int | None = Field(default=None, primary_key=True)
    title: str
    content: str
    published: bool = Field(
        default=True,
        sa_column_kwargs={"server_default": "true"}
    )
    created_at: datetime | None = Field(
    default=None,
    sa_type=TIMESTAMP(timezone=True),
    sa_column_kwargs={"server_default": text("now()"), "nullable": False}
    )
    owner_id: int = Field(foreign_key="users.id", nullable=False, ondelete="CASCADE")
    owner: User | None = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Vote(SQLModel, table=True):
    __tablename__ = "votes"

    user_id: int = Field(foreign_key="users.id", primary_key=True, nullable=False, ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", primary_key=True, nullable=False, ondelete="CASCADE")


