import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from youtube_search import YoutubeSearch
import yt_dlp
from flask import Flask
from threading import Thread

# Bot sozlamalari
TOKEN = "8219536583:AAFIAF_XHr9q1yk07rCzpraG7FMfR6loN64"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render uchun kichik server
app = Flask('')
@app.route('/')
def home(): return "Bot faol!"

def run(): app.run(host='0.0.0.0', port=8080)

def download_audio(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results: return None
    
    video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
    file_name = "music.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music', # Fayl nomi
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return results[0]['title']

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Qo'shiq nomini yuboring, men darhol topib beraman. 🎵")

@dp.message(F.text)
async def search(message: types.Message):
    msg = await message.answer("Qidirilmoqda... 🔍")
    try:
        title = download_audio(message.text)
        if title:
            audio = types.FSInputFile("music.mp3")
            await message.answer_audio(audio, caption=f"🎵 {title}")
            if os.path.exists("music.mp3"): os.remove("music.mp3")
        else:
            await message.answer("Hech narsa topilmadi 😔")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
    finally:
        await msg.delete()

async def main():
    Thread(target=run).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
