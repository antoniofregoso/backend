from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    email: str = Field(unique=True, index=True)
    name: str = Field(nullable=False)
    password: str 
    disabled: bool = Field(default=False)
