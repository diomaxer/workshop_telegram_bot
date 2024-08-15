import asyncio
from pathlib import Path
from typing import List

from dotenv import dotenv_values

from app.internal.repository.sqlite.pictures import create_pictures
from app.pkg import models

settings = dotenv_values()


SRC_VOLUME_PATH = settings.get("SRC_VOLUME_PATH")


class AddPictureWorker:

    async def read_pictures(self) -> List[models.Picture]:
        memes_path = Path(f'{SRC_VOLUME_PATH}/pictures/memes/')
        pictures = []
        for mem in memes_path.iterdir():
            if mem.is_dir():
                mem_path = Path(f'{SRC_VOLUME_PATH}/pictures/memes/{mem.name}/')
                for file in mem_path.iterdir():
                    if file.is_file():
                        pictures.append(
                            models.Picture(name=file.name, type=mem.name)
                        )
        return pictures

    async def run(self):
        print("Start Add Picture Worker!")
        while True:
            try:
                print("Reading pictures folders.")
                pictures = await self.read_pictures()
                await create_pictures(pictures=pictures)
                print("Updated pictures. Wait 5 minutes.")
                await asyncio.sleep(5 * 60)
            except Exception as ex:
                print(ex)
                await asyncio.sleep(60)
