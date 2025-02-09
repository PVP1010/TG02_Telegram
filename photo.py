import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram import F
import asyncio

# Настройка логирования
logging.basicConfig(level=logging.INFO)

from config import TOKEN                             # импортируем токен в основной файл
# Инициализация бота
API_TOKEN = TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем папку для изображений
if not os.path.exists("img"):
    os.makedirs("img")
    logging.info("Папка 'img' создана")


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.reply("Привет! Отправь мне фото, и я сохраню его!")


# Обработчик фотографий
@dp.message(F.content_type == ContentType.PHOTO)
async def save_photo(message: types.Message):
    try:
        photo = message.photo[-1]                                       # Берем фото с самым высоким разрешением
        file = await bot.get_file(photo.file_id)                        # Получаем информацию о файле
        file_path = os.path.join("img", f"{photo.file_id}.jpg")         # Формируем путь для сохранения
        await bot.download_file(file.file_path, destination=file_path)  # Скачиваем файл
        await message.reply("Фото сохранено! ✅")
        logging.info(f"Фото сохранено: {file_path}")

    except Exception as e:
        logging.error(f"Ошибка: {e}")
        await message.reply("Не удалось сохранить фото 😢")



# Создадим асинхронную функцию main, которая будет запускать наш бот:
async def main():                                    # Это асинхронная функция main
    await dp.start_polling(bot)                      # Запуск действия

if __name__ == "__main__":                           # Запуск
    asyncio.run(main())                              # Запуск асинхронной функции main