import asyncio
from datetime import datetime

from app.internal.repository.sqliet_repository import (
    get_today_pictures,
    update_pictures_to_yesterday,
    update_all_type_pictures_to_inactive,
)


class UpdatePictureStatusWorker:

    def __init__(self):
        self.current_day = self.count_day()

    async def count_day(self):
        now = datetime.now().timestamp()
        return int(now // (60 * 60 * 24))

    async def check_day(self):
        day = await self.count_day()
        if await self.current_day < day:
            self.current_day = day
            return True
        return False

    async def update_picture_status(self):
        print("Получаем картинки за сегодня")
        today_pictures = await get_today_pictures()
        today_pictures_ids = []
        types_to_reset = []
        for picture in today_pictures:
            if picture[4]:
                types_to_reset.append(picture[1])
            else:
                today_pictures_ids.append(picture[0])
        if today_pictures_ids:
            print("Обновляем картинки за сегодня")
            await update_pictures_to_yesterday(
                pictures_id=today_pictures_ids
            )
        if types_to_reset:
            print(f"Обноляем все картинки в типах {types_to_reset}")
            await update_all_type_pictures_to_inactive(
                pictures_types=types_to_reset
            )

    async def run(self):
        await asyncio.sleep(9.8)
        while True:
            try:
                if await self.check_day():
                    print(f"Start new day! {datetime.now().strftime('%Y-%m-%d')}")
                    await self.update_picture_status()
                await asyncio.sleep(60)
            except Exception as ex:
                print(ex)
                await asyncio.sleep(60)
