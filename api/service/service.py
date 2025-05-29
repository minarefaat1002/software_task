from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import desc, select, null, asc
from ..models.models import Category
from ..schemas.schemas import CategoryCreate

class CategoryService:
    """
    Service class for handling category-related operations including CRUD operations
    and hierarchical category management.
    """
    
    async def get_root_categories(self, session: AsyncSession) -> list[Category]:
        """
        Retrieves all root categories (categories with no parent).
        
        Args:
            session (AsyncSession): The database session for executing queries.
            
        Returns:
            list[Category]: A list of root categories ordered by creation date (newest first).
        """
        statement = (
                select(Category)
                .where(Category.parent_id == null())
                .order_by(asc(Category.created_at))
                )
        result = await session.exec(statement)
        return result.all()
    
    async def get_children_categories(self, parent_id: int, session: AsyncSession) -> list[Category] | None:
        """
        Retrieves all direct child categories of a specified parent category.
        
        Args:
            parent_id (int): The ID of the parent category.
            session (AsyncSession): The database session for executing queries.
            
        Returns:
            list[Category] | None: A list of child categories ordered by creation date (newest first),
                                  or None if the parent category doesn't exist.
        """
        # Verify parent exists
        parent = await session.get(Category, parent_id)
        if not parent: 
            return None
            
        statement = (
            select(Category)
            .where(Category.parent_id == parent_id)
            .order_by(asc(Category.created_at))
        )
        result = await session.exec(statement)
        return result.all()
     
    async def get_category(self, id: int, session: AsyncSession) -> Category | None:
        """
        Retrieves a single category by its ID.
        
        Args:
            id (int): The ID of the category to retrieve.
            session (AsyncSession): The database session for executing queries.
            
        Returns:
            Category | None: The requested category if found, None otherwise.
        """
        category = await session.get(Category, id)
        return category
    
    async def create_category(self, category_data: CategoryCreate, session: AsyncSession) -> Category | None:
        """
        Creates a new category with the provided data.
        
        Args:
            category_data (CategoryCreate): The data for the new category.
            session (AsyncSession): The database session for executing queries.
            
        Returns:
            Category | None: The newly created category if successful, None if the parent category
                            doesn't exist (for child categories).
                            
        Notes:
            - If the category has a parent_id specified, verifies the parent exists before creation.
            - Automatically sets the creation timestamp.
        """
        # Validate parent exists if this is a child category
        if category_data.parent_id is not None:
            parent_id = category_data.parent_id
            parent = await session.get(Category, parent_id)
            if not parent:
                return None

        # Convert Pydantic model to dictionary and create new Category
        category_data_dict = category_data.model_dump()
        new_category = Category(**category_data_dict)
        
        # Persist to database
        session.add(new_category)
        await session.commit()
        return new_category