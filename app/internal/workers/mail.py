import asyncio
import secrets
from datetime import datetime

import httpx
from dotenv import dotenv_values

from app.internal.repository.sqlite.users import read_all_users

settings = dotenv_values()


MAILING_TIME = int(settings.get("MAILING_TIME"))
BOT_API_TOKEN = settings.get("BOT_API_TOKEN")
USER_GROUP_SIZE = int(settings.get("USER_GROUP_SIZE"))


mail_text = """, искренне приветствуем тебя!\n
Как ты?
Надеемся, что хорошо 💜\n
Смастерим твой день?
Выбирай тему 💫
"""


class MailingWorker:

    def __init__(self):
        self.is_send_today = False

    async def check_hour(self):
        hour = int(datetime.now().strftime("%H"))
        if hour == MAILING_TIME:
            if not self.is_send_today:
                self.is_send_today = True
                return True
        else:
            self.is_send_today = False
        return False

    async def send_message(self, chat_id: str, message: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url=f'https://api.telegram.org/bot{BOT_API_TOKEN}/sendMessage',
                    data={
                        'chat_id': chat_id,
                        'text': message,
                        "parse_mode": "markdown",
                    }
                )
                print(response.json())
            except Exception as ex:
                print(ex)

    async def start_mailing(self):
        users = await read_all_users()
        for users_group in range(0, len(users), USER_GROUP_SIZE):
            await asyncio.gather(
                *[
                    self.send_message(
                        chat_id=user[0],
                        message=f"**{user[1]}**" + mail_text,
                    )
                    for user in users[users_group: users_group + USER_GROUP_SIZE]
                ]
            )
            await asyncio.sleep(secrets.randbelow(50) + 50)

    async def run(self):
        while True:
            try:
                if await self.check_hour():
                    print(f"Start mailing!")
                    await self.start_mailing()
                await asyncio.sleep(60)
            except Exception as ex:
                print(ex)
                await asyncio.sleep(60)

