import asyncio

from src.harmony_hound.adapters.database.connection import connection
from src.harmony_hound.domain.models.users import Users
from sqlalchemy import select

@connection
async def add_users(session):
    user = Users(
        first_name='David',
        last_name='Smaev',
        username='SDavid',
        lang='RU'
    )

    session.add(user)

    await session.commit()

@connection
async def get_users(session):
    records = await session.execute(select(Users))
    results = records.scalars().unique().all()

    return results

async def bot_main():
    await add_users()

    users : List[Users] = await get_users()

    print(f"Get all users {users}")


if __name__ == '__main__':
    asyncio.run(bot_main())


