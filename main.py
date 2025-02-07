import asyncio
from aiogram import Bot, Dispatcher, F
# Для обработки команд импортируем нужные фильтры и типы сообщений:
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile
import random

from gtts import gTTS
import os


from config import TOKEN                             # импортируем токен в основной файл                                       # импортируем модуль random

# Создадим объекты классов Bot и Dispatcher:
bot = Bot(token=TOKEN)                               #  Bot отвечает за взаимодействие с Telegram bot API
dp = Dispatcher()                                    #  Dispatcher управляет обработкой входящих сообщений и команд.


@dp.message(Command('voice'))                                  # функция голос команды /voice
async def voice(message: Message):
    voice = FSInputFile("sample.ogg")                          # Сохраняем голосовой файл в переменную voice
    await message.answer_voice(voice)                          # Отправляем голос в ответ на команду /voice

@dp.message(Command('doc'))                                   # функция документ команды /doc
async def doc(message: Message):
    doc = FSInputFile("TG02.txt")
    await bot.send_document(message.chat.id, doc)




@dp.message(Command('video'))                        # функция видео команды /video
async def video(message: Message):
    await bot.send_chat_action(message.chat.id, 'upload_video')   # Загрузка видео
    video = FSInputFile('video.mp4')                                    # Отправляем видео
    await bot.send_video(message.chat.id, video)


@dp.message(Command('audio'))                        # функция аудио команды /audio
async def audio(message: Message):
    audio = FSInputFile('sound1.mp3')
    await bot.send_audio(message.chat.id, audio)


@dp.message(Command('training'))
async def training(message: Message):                # функция тренировка команда /training
   training_list = [
       "Тренировка 1:\n1. Скручивания: 3 подхода по 15 повторений\n2. Велосипед: 3 подхода по 20 повторений (каждая сторона)\n3. Планка: 3 подхода по 30 секунд",
       "Тренировка 2:\n1. Подъемы ног: 3 подхода по 15 повторений\n2. Русский твист: 3 подхода по 20 повторений (каждая сторона)\n3. Планка с поднятой ногой: 3 подхода по 20 секунд (каждая нога)",
       "Тренировка 3:\n1. Скручивания с поднятыми ногами: 3 подхода по 15 повторений\n2. Горизонтальные ножницы: 3 подхода по 20 повторений\n3. Боковая планка: 3 подхода по 20 секунд (каждая сторона)"
   ]
   rand_tr = random.choice(training_list)                                    # Ввыодим случайную тренировку
   await message.answer(f"Это ваша мини-тренировка на сегодня\n {rand_tr}")    # Ответ бота на команду /training

   tts = gTTS(text=rand_tr, lang='ru')                                       # Преобразуем текст в аудио
   tts.save('training.mp3')                                                  # Сохраняем аудио
   audio = FSInputFile('training.mp3')                                       # сохраняем аудио в переменную audio
   await bot.send_audio(message.chat.id, audio)                              # Отправляем аудио
   os.remove('training.mp3')                                                 # Удаляем аудио


@dp.message(Command("photo"))                        # функция фото команды /photo
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
    await bot.download(message.photo[-1], destination=f'tmp/{message.photo[-1].file_id}.jpg') # Скачиваем фото


@dp.message(F.text == "Что такое ИИ?")               # Обработка команды "Что такое ИИ?"
async def aitext(message: Message):
    await message.answer("Искусственный интеллект (ИИ) — это область компьютерных наук, которая занимается созданием систем и алгоритмов, способных выполнять задачи, требующие **человеческого интеллекта**. Эти задачи включают обучение, распознавание образов, понимание естественного языка, принятие решений и даже творчество.")




@dp.message(Command("help"))                         # Обработка команды /help
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды: \n /start" "\n /help" "\n /photo")  # Ответ бота на команду /help

# Создадим декоратор для обработки команды /start:
# Вместо "я бот" напишем "привет" и укажем имя пользователя
@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}')


# Создадим асинхронную функцию main, которая будет запускать наш бот:
async def main():                                    # Это асинхронная функция main
    await dp.start_polling(bot)                      # Запуск действия

if __name__ == "__main__":                           # Запуск
    asyncio.run(main())                              # Запуск асинхронной функции main