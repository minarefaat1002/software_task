from fastapi.responses import Response
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException 
from fastapi import Query, Path
from typing import List, Optional
from ..service.service import CategoryService
from ..schemas.schemas import CategoryRead, CategoryCreate
from sqlmodel.ext.asyncio.session import AsyncSession
from ..db.db import get_session

# Initialize API router and service
category_router = APIRouter()
category_service = CategoryService()

@category_router.get(
    "/",
    response_model=List[CategoryRead],
    summary="Get categories",
    description="""Retrieve categories from the system. 
    If no parent_id is provided, returns root categories.
    When parent_id is provided, returns children of that category.""",
    responses={
        200: {"description": "List of categories returned successfully"},
        404: {"description": "Parent category not found"}
    }
)
async def get_children(
    parent_id: Optional[int] = Query(
        None, 
        description="ID of parent category. Omit to get root categories",
        example=1
    ), 
    session: AsyncSession = Depends(get_session)
) -> List[CategoryRead]:
    """
    Retrieve categories based on parent-child relationship.
    
    Args:
        parent_id: Optional parent category ID to filter children
        session: Async database session dependency
        
    Returns:
        List of CategoryRead objects
        
    Raises:
        HTTPException 404: If specified parent category doesn't exist
    """
    if parent_id is None:
        # Return root categories (where parent_id is NULL)
        categories = await category_service.get_root_categories(session)
        return categories
    
    categories = await category_service.get_children_categories(parent_id, session)
    if categories is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent category with ID {parent_id} not found"
        )
    return categories

@category_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=CategoryRead,
    summary="Create new category",
    description="Create a new category with the provided data",
    responses={
        201: {"description": "Category created successfully"},
        404: {"description": "Specified parent category doesn't exist"},
        422: {"description": "Validation error in request body"}
    }
)
async def create_category(
    category_data: CategoryCreate,
    session: AsyncSession = Depends(get_session),
) -> CategoryRead:
    """
    Create a new category in the system.
    
    Args:
        category_data: Category creation data including name and optional parent_id
        session: Async database session dependency
        
    Returns:
        The newly created category with generated ID
        
    Raises:
        HTTPException 404: If specified parent_id doesn't exist
    """
    new_category = await category_service.create_category(category_data, session)
    if new_category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Parent category with ID {category_data.parent_id} not found"
        )
    return new_category

@category_router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete category",
    description="Delete a category by ID if it has no children",
    responses={
        204: {"description": "Category deleted successfully"},
        400: {"description": "Category has children and cannot be deleted"},
        404: {"description": "Category not found"}
    }
)
async def delete_category(
    id: int = Path(..., description="ID of category to delete", example=1),
    session: AsyncSession = Depends(get_session),
) -> None:
    """
    Delete a category from the system.
    
    Args:
        id: ID of the category to delete
        session: Async database session dependency
        
    Raises:
        HTTPException 404: If category doesn't exist
        HTTPException 400: If category has children
    """
    category = await category_service.get_category(id, session)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Category with id {id} doesn't exist."
        )
        
    # Explicitly load children relationship
    await session.refresh(category, attribute_names=["children"])
    if category.children:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"The category with id {id} has children. It cannot be removed."
        )
        
    await session.delete(category)
    await session.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)