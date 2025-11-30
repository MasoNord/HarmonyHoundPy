from src.harmony_hound.application.common.settings import settings
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

DATABASE_URL = settings.get_db_url()

engine = create_async_engine(url=DATABASE_URL)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

def connection(method):
    async def wrapper(*args, **kwargs):
        async with async_session_maker() as session:
            try:
                return await method(*args, **kwargs, session=session)
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    return wrapper