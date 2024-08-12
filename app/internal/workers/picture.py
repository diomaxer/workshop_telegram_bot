import asyncio
import aiosqlite


async def create_database():
    async with aiosqlite.connect(SQLITE_PATH) as db:
        await db.execute(
            """create table if not exists pictures(
                id integer primary key,
                name text,
                type text,
                is_active bool
            )"""
        )
        await db.commit()


async def read_pictures(name, type, is_active):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        await db.execute(
            "insert into pictures(name, type, is_active) values(?, ?, ?)",
            (name, type, is_active)
        )
        await db.commit()

async def root():
    await create_database()


if __name__ == '__main__':
    asyncio.run(root())