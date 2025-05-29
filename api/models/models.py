from datetime import datetime 
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship, text

class Category(SQLModel, table=True):
    """
    SQLModel class representing a Category entity in the database.
    
    Implements a self-referential hierarchical relationship allowing categories
    to have parent-child relationships (for building category trees).
    
    Attributes:
        id: Primary key identifier
        name: Category display name
        parent_id: Reference to parent category (for hierarchy)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
        parent: Relationship to parent category
        children: List of child categories
    """ 
    __tablename__ = "categories"
     
    # Primary key
    id: Optional[int] = Field( 
        default=None,
        primary_key=True,
    )
     
    # Basic fields
    name: str = Field(
        ...,
        min_length=1,
        max_length=100
    )
    
    # Relationship field
    parent_id: Optional[int] = Field(
        default=None,
        foreign_key="categories.id",
    )
    
    # Timestamp fields
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"server_default": text("CURRENT_TIMESTAMP")}
    )
    
    # Relationship configurations
    parent: Optional["Category"] = Relationship(
        back_populates="children",
        sa_relationship_kwargs={
            "remote_side": "Category.id",
            "cascade": "save-update, merge"
        }, 
    )
    
    children: list["Category"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "lazy": "selectin"
        },
    )

    def __repr__(self) -> str:
        """String representation of the Category instance"""
        return f"<Category(id={self.id}, name='{self.name}')>"