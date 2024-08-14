from typing import List

import aiosqlite

from app.pkg import models
from dotenv import dotenv_values

settings = dotenv_values()

SQLITE_URL = settings.get("SQLITE_URL")


async def create_database():
    async with aiosqlite.connect(SQLITE_URL) as db:
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


async def create_pictures(pictures: List[models.Picture]):
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            insert into pictures(name, type, is_active) values(?, ?, ?)
                on conflict(name) do nothing;
        """
        for picture in pictures:
            await db.execute(query, (picture.name, picture.type, picture.is_active))
            await db.commit()


async def get_picture_by_type(picture_type: str):
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            select id, min(name) from pictures 
                where type = ? and is_active = false
            limit 1;
        """
        async with db.execute(query, (picture_type,)) as cursor:
            return await cursor.fetchone()


async def get_today_pictures():
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            select
                coalesce(t3.id, 0) as id,
                t1.type,
                coalesce(t3.name, 'name') as name,
                coalesce(t3.is_active, 0) as is_active,
                case
                    when t2.min_name is null then 1
                    else 0
                end as is_empty
            from
                (select distinct type from pictures) t1
            left join
                (
                    select type, min(name) as min_name
                    from pictures
                    where is_active = 0
                    group by type
                ) t2
            on t1.type = t2.type
            left join
                pictures t3
            on t2.type = t3.type and t2.min_name = t3.name
            order by t1.type;
        """
        async with db.execute(query) as cursor:
            return await cursor.fetchall()


async def update_pictures_to_yesterday(pictures_id: List[int]):
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            update pictures
                set is_active = true, last_used = current_timestamp
            where id in (?);
        """
        for picture_id in pictures_id:
            await db.execute(query, (picture_id,))
            await db.commit()


async def update_all_type_pictures_to_inactive(pictures_types: List[str]):
    async with aiosqlite.connect(SQLITE_URL) as db:
        query = """
            update pictures
                set is_active = false
            where type = (?);
        """
        for pictures_type in pictures_types:
            await db.execute(query, (pictures_type,))
            await db.commit()


