from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import EmailStr, constr

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    email: EmailStr = Field(unique=True, index=True)
    name: constr(min_length=2, max_length=100)
    password: constr(min_length=8)
    disabled: bool = Field(default=False)
