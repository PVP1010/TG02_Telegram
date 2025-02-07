import asyncio
from aiogram import Bot, Dispatcher, F
# Для обработки команд импортируем нужные фильтры и типы сообщений:
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN                             # импортируем токен в основной файл
import random                                        # импортируем модуль random

# Создадим объекты классов Bot и Dispatcher:
bot = Bot(token=TOKEN)                               #  Bot отвечает за взаимодействие с Telegram bot API
dp = Dispatcher()                                    #  Dispatcher управляет обработкой входящих сообщений и команд.

@dp.message(Command("photo"))                        # Обработка команды /help
async def photo(message: Message):                   # Список ответов
    list = ['https://avatars.mds.yandex.net/i?id=9b513a670ee76376548f34a5c5660345589baf4d-9870356-images-thumbs&n=13',
            'https://avatars.mds.yandex.net/i?id=9c06b52cd440474f4866a3a5cc69d03bf0201fd6-7663084-images-thumbs&n=13',
            'https://avatars.mds.yandex.net/i?id=75c8f5559d1e51bddc7fac372513731b-5250945-images-thumbs&n=13'
    ]
    rand_photo = random.choice(list)
    await message.answer_photo(photo=rand_photo, caption="Это рандомная фотка")


@dp.message(F.photo)                                 # Обработка фото
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше'] # Список ответов
    rand_answer = random.choice(list)                # Выбор случайного ответа
    await message.answer(rand_answer)                # Ответ бота



@dp.message(F.text == "Что такое ИИ?")               # Обработка команды "Что такое ИИ?"
async def aitext(message: Message):
    await message.answer("Искусственный интеллект (ИИ) — это область компьютерных наук, которая занимается созданием систем и алгоритмов, способных выполнять задачи, требующие **человеческого интеллекта**. Эти задачи включают обучение, распознавание образов, понимание естественного языка, принятие решений и даже творчество.")




@dp.message(Command("help"))                         # Обработка команды /help
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start" "\n /help" "\n /photo")  # Ответ бота на команду /help

# Создадим декоратор для обработки команды /start:
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Приветики, я бот!")

# Пустой декоратор для обработки любых сообщений:
@dp.message()
async def start(message: Message):
    await message.answer("Не беспокой меня по пустякам!")

# Создадим асинхронную функцию main, которая будет запускать наш бот:
async def main():                                    # Это асинхронная функция main
    await dp.start_polling(bot)                      # Запуск действия

if __name__ == "__main__":                           # Запуск
    asyncio.run(main())                              # Запуск асинхронной функции main