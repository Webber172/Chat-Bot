import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

TOKEN = os.getenv("BOT_TOKEN")  # токен берётся из Railway variables

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Пришли ссылку на YouTube-видео — я отправлю аудио 🎧")

@dp.message()
async def download_audio(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Скачиваю аудио...")

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "audio.%(ext)s",
        "quiet": True,
        "noplaylist": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await message.answer_document(
            types.FSInputFile(filename),
            caption="✅ Готово"
        )

        os.remove(filename)

    except Exception as e:
        await message.answer(f"❌ Ошибка: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
