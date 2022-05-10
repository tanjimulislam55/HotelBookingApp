from sqlalchemy.ext.asyncio import AsyncSession
from db.config import async_session

async def get_session() -> AsyncSession:
        print("*" * 50)
        print("Get DB CALLED")
        print("*" * 50)
        async with async_session() as session:
            # async with session.begin():
            print("*" * 50)
            print("Session Yielded")
            print("*" * 50)
            yield session