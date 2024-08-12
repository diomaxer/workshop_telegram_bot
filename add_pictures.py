import asyncio
from datetime import datetime
from pathlib import Path

from app.internal.repository.sqliet_repository import *


class UpdatePictureWorker:

    def __init__(self):
        self.current_day = 0

    async def read_pictures(self) -> List[models.Picture]:
        memes_path = Path('src/pictures/memes/')
        pictures = []
        for mem in memes_path.iterdir():
            if mem.is_dir():
                mem_path = Path(f'src/pictures/memes/{mem.name}/')
                for file in mem_path.iterdir():
                    if file.is_file():
                        pictures.append(
                            models.Picture(name=file.name, type=mem.name)
                        )
        return pictures

    async def update_pictures(self):
        day = datetime.now().timestamp() // (60 * 60 * 24)
        if self.current_day < day:
            pictures = await get_today_pictures()
            if pictures:
                await update_pictures_to_yesterday(pictures=pictures)
                return
            await update_all_pictures_to_inactive(pictures=pictures)


    async def run(self):
        print("Start pictures worker!")
        await create_database()
        print("Create pictures database.")
        while True:
            try:
                # await self.update_pictures()
                pictures = await self.read_pictures()
                print("Updating pictures.")
                await create_pictures(pictures=pictures)
                await asyncio.sleep(5 * 60)
            except Exception as ex:
                print(ex)
                await asyncio.sleep(60)


if __name__ == '__main__':
    worker = UpdatePictureWorker()
    asyncio.run(worker.run())
