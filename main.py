import logging
import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ContentType
from googletrans import Translator
from aiogram import F

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Твой токен бота
from config import TOKEN  # Убедись, что в config.py есть переменная TOKEN

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher()
translator = Translator()

# Создаем папку для голосовых сообщений
if not os.path.exists("voice"):
    os.makedirs("voice")
    logging.info("Папка 'voice' создана")


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Отправь мне голосовое сообщение или напиши текст для перевода!")


# Обработчик голосовых сообщений
@dp.message(F.content_type == ContentType.VOICE)
async def handle_voice(message: types.Message):
    try:
        voice = message.voice  # Получаем голосовое сообщение
        file = await bot.get_file(voice.file_id)  # Получаем информацию о файле
        file_path = os.path.join("voice", f"{voice.file_id}.ogg")  # Формируем путь сохранения
        await bot.download_file(file.file_path, destination=file_path)  # Сохраняем файл

        await message.reply("Голосовое сообщение сохранено! 🎤")
        logging.info(f"Голосовое сообщение сохранено: {file_path}")

        # Отправляем голосовое сообщение обратно пользователю
        with open(file_path, "rb") as voice_file:
            await message.answer_voice(voice_file)

    except Exception as e:
        logging.error(f"Ошибка при обработке голосового: {e}")
        await message.reply("Не удалось сохранить голосовое сообщение 😢")


# Обработчик текстовых сообщений (перевод на английский)
@dp.message()
async def translate_text(message: types.Message):
    try:
        translated = translator.translate(message.text, dest="en")  # Переводим текст
        await message.reply(f"Перевод на английский:\n**{translated.text}**")
    except Exception as e:
        logging.error(f"Ошибка перевода: {e}")
        await message.reply("Ошибка перевода 😢")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
