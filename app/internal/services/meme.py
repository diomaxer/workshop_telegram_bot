from pathlib import Path
from dotenv import dotenv_values

from aiogram import Bot, Dispatcher, html
from aiogram.utils.markdown import hlink
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types
from app.internal.repository.sqliet_repository import get_picture_by_type

settings = dotenv_values()

dp = Dispatcher()
bot = Bot(
    token=settings.get("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


welcome_text = f""", рады знакомству 🙏\n
Мы — {html.bold('Мастер и Скайя')}\n
Нас создали, чтобы мы общались с тобой чаще и помогали мастерить настроение твоего дня.\n
Выбери тему, которая тебе нравится, и мы поделимся с тобой радостью, мыслями и идеями из нашего виртуального мира!\n
В любое время заходи к нам {hlink('в гости. Мы рады друзьям ☑️', 'https://t.me/masterskayadialogov')}\n
Погнали! 💭\n
"""


@dp.message(
    lambda message: message.text in (
        "Мотивация", "Психология", "Любовь", "Юмор", "Паппилэнд"
    )
)
async def button1_handler(message: types.Message):
    memes = {
        "Мотивация": "motivation",
        "Психология": "psychology",
        "Любовь": "love",
        "Юмор": "humour",
        "Паппилэнд": "animals",
    }

    folder_path = Path(f'src/pictures/memes/{memes[message.text]}/')
    picture_name = await get_picture_by_type(picture_type=memes[message.text])
    start_picture = FSInputFile(path=folder_path / picture_name[1])
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=start_picture,
    )


@dp.message(
    lambda message: message.text == "Начало"
)
async def start_button_handler(message: types.Message):
    await command_start_handler(message=message)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    start_picture = FSInputFile("src/pictures/project/start.png")
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Мотивация"),
        KeyboardButton(text="Психология"),
    )
    builder.row(
        KeyboardButton(text="Любовь"),
        KeyboardButton(text="Юмор"),
        KeyboardButton(text="Паппилэнд"),
    )
    builder.row(
        KeyboardButton(text="Начало"),
    )
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=start_picture,
        caption=html.bold(message.from_user.full_name) + welcome_text,
        reply_markup=builder.as_markup(
            resize_keyboard=True
        ),
    )
