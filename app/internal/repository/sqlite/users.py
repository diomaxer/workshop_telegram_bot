import aiosqlite
from app.pkg import models
from dotenv import dotenv_values

settings = dotenv_values()

SQLITE_URL = settings.get("SQLITE_URL")


async def create_users_table():
    async with aiosqlite.connect(SQLITE_URL) as db:
        await db.execute(
            """
            create table if not exists users(
                id integer primary key,
                chat_id integer unique not null,
                name text not null,
                is_active bool not null default True
            );
        """
        )
        await db.commit()


async def create_user(user: models.User):
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            insert into users(chat_id, name, is_active) values(?, ?, ?)
                on conflict(chat_id) do nothing;
        """
        await db.execute(query, (user.chat_id, user.name, user.is_active))
        await db.commit()


async def read_all_users():
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            select chat_id, name from users
                where is_active in (true);
        """
        async with db.execute(query) as cursor:
            return await cursor.fetchall()
