from pathlib import Path

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hlink
from dotenv import dotenv_values

from app.internal.repository.sqlite.pictures import get_picture_by_type
from app.internal.repository.sqlite.users import create_user
from app.pkg import models

settings = dotenv_values()

dp = Dispatcher()
bot = Bot(
    token=settings.get("BOT_API_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

SRC_VOLUME_PATH = settings.get("SRC_VOLUME_PATH")


welcome_text = f""", рады знакомству 🙏\n
Мы — {html.bold('Мастер и Скайя')}\n
Нас создали, чтобы мы общались с тобой чаще и помогали мастерить настроение твоего дня.\n
Выбери тему, которая тебе нравится, и мы поделимся с тобой радостью, мыслями и идеями из нашего виртуального мира!\n
В любое время заходи к нам {hlink('в гости. Мы рады друзьям ☑️', 'https://t.me/masterskayadialogov')}\n
Погнали! 💭\n
"""

picture_text = f"""Выбирай другую тему или возвращайся завтра за новой порцией настроения 💫"""


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
        caption=picture_text
    )


@dp.message(
    lambda message: message.text == "Начало"
)
async def start_button_handler(message: types.Message):
    await command_start_handler(message=message)


async def build_keyboard() -> ReplyKeyboardBuilder:
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
    return builder


async def record_user(message: types.Message):
    try:
        user = models.User(
            chat_id=message.chat.id,
            name=message.from_user.full_name,
            is_active=True
        )
        await create_user(user=user)
    except Exception as ex:
        print(ex)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await record_user(message=message)

    builder = await build_keyboard()
    await bot.send_photo(
        chat_id=message.chat.id,
        photo=FSInputFile(f"{SRC_VOLUME_PATH}/pictures/project/start.png"),
        caption=html.bold(message.from_user.full_name) + welcome_text,
        reply_markup=builder.as_markup(
            resize_keyboard=True
        ),
    )
