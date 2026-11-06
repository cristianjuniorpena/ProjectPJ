from datetime import datetime
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class PostCreate(BaseModel):
    title: str = Field(min_length=3, max_length=150)
    description: str = Field(min_length=10)
    category: str = Field(min_length=2, max_length=100)
    budget: Decimal | None = Field(default=None, ge=0)


class PostUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=3, max_length=150)
    description: str | None = Field(default=None, min_length=10)
    category: str | None = Field(default=None, min_length=2, max_length=100)
    budget: Decimal | None = Field(default=None, ge=0)
    status: Literal["open", "closed"] | None = None

class PostRead(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    category: str
    budget: Decimal | None
    status: Literal["open", "closed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)