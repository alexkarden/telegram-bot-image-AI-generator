import logging
import os
import random

from blossom_ai import Blossom
from mtranslate import translate


ai = Blossom()


def bot_translate(text: str) -> str:
    try:
        translated_text = translate(text, "[english]", "auto")
        return translated_text
    except Exception as e:
        logging.exception("Ошибка при переводе промпта %s", e)
        return None


async def image_generated(translated_text: str, telegramid: int) -> bool:
    seed = telegramid + random.randint(0, 100)
    try:
        await ai.image.save(
            prompt=translated_text[:200],
            filename=f"{telegramid}.jpg",
            model="flux",
            seed=seed,
            width=1024,
            height=1024,
            private=True,
            nologo=True,
        )
        return True
    except Exception as e:
        logging.exception("Ошибка при генерации картинки %s", e)
        return False


def delete_file(file_path: str) -> bool:
    try:
        os.remove(file_path)
        return True
    except Exception as e:
        logging.exception("Ошибка при удалении документа %s", e)
        return False
