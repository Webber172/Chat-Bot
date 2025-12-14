import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from yt_dlp import YoutubeDL
from aiogram.client.session.aiohttp import AiohttpSession

# Получаем токен из переменной окружения
TOKEN = os.getenv("BOT_TOKEN")

if TOKEN is None:
    raise ValueError("Не найден токен! Задайте переменную окружения BOT_TOKEN.")

# Создаём объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.answer("Привет! Отправь ссылку на YouTube, и я пришлю аудио в MP3.")

# Обработчик текстовых сообщений (ссылки)
@dp.message(F.text)
async def download_audio(message: Message):
    url = message.text.strip()
    await message.answer("Скачиваю аудио... ⏳")

    # Настройки yt-dlp для MP3
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'noplaylist': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        # Отправляем MP3 пользователю
        with open(filename, 'rb') as f:
            await message.answer_document(f)

        # Удаляем файл после отправки
        os.remove(filename)

    except Exception as e:
        await message.answer(f"Ошибка при скачивании: {e}")

# Запуск бота
async def main():
    bot.session = AiohttpSession()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
