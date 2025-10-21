from aiogram import F, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile, Message
from dotenv import load_dotenv

from script import bot_translate, delete_file, image_generated


load_dotenv()
router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        "👋 <b>Добро пожаловать!</b>\n\n"
        "Бот умеет генерировать картинки по текстовому промпту\n\n"
        "Просто отправьте боту текст (не более 200 символов) и бот сгенерирует картинку"
    )
    await message.answer(f"{welcome_text}", parse_mode=ParseMode.HTML)


# Обрабатываем исключительно текстовые сообщения (чтобы не перехватывать документы/фото)
@router.message(F.content_type == types.ContentType.TEXT)
async def all_message(message: Message):
    await message.answer("Генерируем.....")
    text = str(message.text)
    en_prompt = bot_translate(text)
    if en_prompt and await image_generated(en_prompt, message.from_user.id) == True:
        photo = FSInputFile(f"{message.from_user.id}.jpg")
        await message.answer_photo(photo=photo, caption=text, parse_mode=ParseMode.HTML)
        delete_file(f"{message.from_user.id}.jpg")
    else:
        await message.answer("'Sad but True' - cервер перегружен, попробуйте позже.")
