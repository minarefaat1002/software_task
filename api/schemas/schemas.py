from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class CategoryBase(SQLModel):
    """
    Base schema for Category with essential fields and validation.
    Used as foundation for other category schemas.
    """
    name: str = Field(
        ...,  # Required field
        min_length=1,
        max_length=100,
        description="The name of the category (1-100 characters)"
    )

    class Config:
        """Pydantic configuration for the base model"""
        extra = "forbid"  # Prevent extra fields during model initialization


class CategoryCreate(CategoryBase):
    """
    Schema for creating new categories.
    Extends CategoryBase with optional parent category reference.
    """
    parent_id: Optional[int] = Field(
        None,
        description="ID of the parent category. Set to null for root categories (no parent)"
    )


class CategoryRead(CategoryBase):
    """
    Schema for reading/returning category data.
    Extends CategoryBase with the database ID and parent reference.
    """
    id: int = Field(..., description="Unique identifier for the category")
    parent_id: Optional[int] = Field(
        None,
        description="ID of the parent category, or null if this is a root category"
    )