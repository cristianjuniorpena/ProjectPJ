
from pydantic import BaseModel, ConfigDict, Field, model_validator
from decimal import Decimal
from typing import Literal
from datetime import datetime


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

    @model_validator(mode="after")
    def validate_non_nullable_fields(self):
        non_nullable = {"title", "description", "category", "status"}

        for field in non_nullable:
            if field in self.model_fields_set and getattr(self, field) is None:
                raise ValueError(f"{field} cannot be null")

        return self
    
# class PostRead(BaseModel):
#     id: int
#     user_id: int
#     title: str
#     description: str
#     category: str
#     budget: Decimal | None
#     status: Literal["open", "closed"]
#     created_at: datetime
#     updated_at: datetime

#     model_config = ConfigDict(from_attributes=True)    

class ContractorPublic(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

class PostRead(BaseModel):
    id: int
    user_id: int

    contractor: ContractorPublic = Field(
        validation_alias="user"
    )

    title: str
    description: str
    category: str
    budget: Decimal | None
    status: Literal["open", "closed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PostReadAllPosts(BaseModel):
    id: int
    user_id: int
    contractor: ContractorPublic

    title: str
    description: str
    category: str
    budget: Decimal | None
    status: Literal["open", "closed"]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

