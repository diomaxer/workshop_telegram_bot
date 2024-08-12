from typing import List

import aiosqlite

from app.pkg import models


async def create_database():
    async with aiosqlite.connect(SQLITE_PATH) as db:
        await db.execute("""
            create table if not exists pictures(
                id integer primary key,
                name text unique not null,
                type text not null,
                is_active bool default False,
                updated_at datetime default current_timestamp,
                last_used datetime defult none
            );
        """
        )
        await db.commit()


async def get_picture_by_type(picture_type: str):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        async with db.execute(
            """
                select id, name from pictures
                    where type = ? and is_active = false and last_used is null
                order by updated_at, name
                limit 1;
            """,
            ((picture_type,))
        ) as cursor:
            return await cursor.fetchone()


async def get_today_pictures():
    async with aiosqlite.connect(SQLITE_PATH) as db:
        async with db.execute(
            """
            SELECT t1.*
                FROM your_table_name t1
                JOIN (
                    SELECT type, MIN(name) as min_name
                    FROM your_table_name
                    WHERE is_active = 0
                    GROUP BY type
                ) t2 ON t1.type = t2.type AND t1.name = t2.min_name
                WHERE t1.is_active = 0;
            """
        ) as cursor:
            return await cursor.fetchall()


async def create_pictures(pictures: List[models.Picture]):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        query = """
            insert into pictures(name, type, is_active) values(?, ?, ?)
                on conflict(name) do nothing;
        """
        for picture in pictures:
            await db.execute(
                query, (picture.name, picture.type, picture.is_active)
            )
            await db.commit()


async def update_pictures(pictures: List[models.Picture]):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        query = """
            insert into pictures(name, type, is_active) values(?, ?, ?)
                on conflict(name) do nothing;
        """
        for picture in pictures:
            await db.execute(
                query, (picture.name, picture.type, picture.is_active)
            )
            await db.commit()


async def update_pictures_to_yesterday(pictures: List[models.Picture]):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        query = """
            insert into pictures(name, type, is_active) values(?, ?, ?)
                on conflict(name) do nothing;
        """
        for picture in pictures:
            await db.execute(
                query, (picture.name, picture.type, picture.is_active)
            )
            await db.commit()


async def update_all_pictures_to_inactive(pictures: List[models.Picture]):
    async with aiosqlite.connect(SQLITE_PATH) as db:
        query = """
            update pictures
                set is_active = false
        """
        await db.execute(query)
        await db.commit()


