import asyncio

from app.internal.repository.sqlite.pictures import create_pictures_table
from app.internal.repository.sqlite.users import create_users_table
from app.internal.services.meme import dp, bot
from app.internal.workers.add_picture import AddPictureWorker
from app.internal.workers.mail import MailingWorker
from app.internal.workers.update_picture_status import UpdatePictureStatusWorker


async def create_tables():
    print("Create tables.")
    await create_users_table()
    await create_pictures_table()


async def run():
    await create_tables()
    print("Launch Telegram Workshop BOT!")
    add_picture_worker = AddPictureWorker()
    update_picture_status_worker = UpdatePictureStatusWorker()
    main_worker = MailingWorker()
    await asyncio.gather(
        dp.start_polling(bot),
        add_picture_worker.run(),
        update_picture_status_worker.run(),
        main_worker.run()
    )


if __name__ == "__main__":
    asyncio.run(run())
