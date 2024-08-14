import asyncio

from app.internal.services.meme import dp, bot
from app.internal.workers.add_picture_worker import AddPictureWorker
from app.internal.workers.update_picture_status import UpdatePictureStatusWorker


async def run():
    print("Launch Telegram Workshop BOT!")
    add_picture_worker = AddPictureWorker()
    update_picture_status_worker = UpdatePictureStatusWorker()
    await asyncio.gather(
        dp.start_polling(bot),
        add_picture_worker.run(),
        update_picture_status_worker.run(),
    )


if __name__ == "__main__":
    asyncio.run(run())
