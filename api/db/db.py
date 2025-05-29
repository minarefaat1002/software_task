from sqlmodel import SQLModel, select
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from ..config import Config
from ..models.models import Category
from sqlmodel.ext.asyncio.session import AsyncSession
# Create an async database engine instance
engine = create_async_engine(
    url=Config.DATABASE_URL,  # Database connection URL from configuration
    echo=True,  # Enable SQL query logging for debugging
    pool_size=20,  # Number of connections to keep in pool
    max_overflow=10,  # Maximum number of connections beyond pool_size
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_recycle=3600  # Recycle connections after 1 hour
)

async def init_db() -> None:
    """
    Initialize the database by creating all tables defined in SQLModel metadata.
    
    Usage:
        await init_db()
    """
    async with engine.begin() as connection:
        # Create all tables if they don't exist
        await connection.run_sync(SQLModel.metadata.create_all)
    await insert_dummy_data()


async def get_session() -> AsyncSession:
    """
    Async generator function that yields database sessions.
    
    Yields:
        AsyncSession: An asynchronous database session
        
    Usage:
        async with get_session() as session:
            # Use session for database operations
            result = await session.execute(query)
    """
    # Configure session factory with our engine
    Session = sessionmaker(
        bind=engine,  # Use our async engine
        class_=AsyncSession,  # Create async sessions
        expire_on_commit=False,  # Keep objects loaded after commit
        autoflush=False  # Disable autoflush for better control
    )
    
    async with Session() as session:
        yield session  # Provide session to the caller


async def insert_dummy_data():
    session_generator = get_session()
    session = await session_generator.__anext__()
    category_1 = await session.execute(
        select(Category).where(Category.id == 1)
    )
    # if the dummy data inserted before then there's no need to inert them again.
    if category_1.scalar() is not None:
        return
    session.add(Category(name="category A"))
    session.add(Category(name="category B"))
    session.add(Category(name="category C"))
    session.add(Category(parent_id=1, name="subcategory A1"))
    session.add(Category(parent_id=1, name="subcategory A2"))
    session.add(Category(parent_id=1, name="subcategory A3"))
    session.add(Category(parent_id=4, name="sub subcategory A1-1"))
    session.add(Category(parent_id=4, name="sub subcategory A1-2"))
    session.add(Category(parent_id=2, name="subcategory B1"))
    session.add(Category(parent_id=2, name="subcategory B2"))
    session.add(Category(parent_id=2, name="subcategory B3"))
    session.add(Category(parent_id=3, name="subcategory C1"))
    await session.commit()
   
 
 