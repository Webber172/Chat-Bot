import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("8287498125:AAFVZvSTbBagW5NgQWVkrmb5u965skBTgQk")


bot = Bot(token=TOKEN)
dp = Dispatcher()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def download_mp3(url: str) -> str:
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_DIR}/%(title)s.%(ext)s",
        "quiet": True,
        "noplaylist": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info).rsplit(".", 1)[0] + ".mp3"

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Отправь ссылку на YouTube-видео.")

@dp.message()
async def handle_link(message: types.Message):
    url = message.text.strip()

    if "youtube.com" not in url and "youtu.be" not in url:
        await message.answer("Отправь ссылку на YouTube.")
        return

    await message.answer("🎵 Скачиваю аудио, подожди...")

    try:
        loop = asyncio.get_running_loop()
        file_path = await loop.run_in_executor(
            None, download_mp3, url
        )

        await message.answer_audio(
            audio=FSInputFile(file_path),
            title=os.path.basename(file_path)
        )

        os.remove(file_path)

    except Exception as e:
        await message.answer("❌ Ошибка при загрузке аудио.")
        print(e)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())