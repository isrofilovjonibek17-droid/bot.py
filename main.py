import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from youtube_search import YoutubeSearch
import yt_dlp
from flask import Flask
from threading import Thread

# Bot tokenini o'zgaruvchiga olamiz
TOKEN = "8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render.com o'chib qolmasligi uchun kichik Flask server
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Musiqa qidirish va yuklash funksiyasi
def download_audio(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        return None
    
    url = f"https://www.youtube.com{results[0]['url_suffix']}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.mp3',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return results[0]['title']

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Salom! Qo'shiq nomini yuboring, men uni topib beraman.")

@dp.message()
async def search_music(message: types.Message):
    msg = await message.answer("Qidirilmoqda... 🔍")
    try:
        title = download_audio(message.text)
        if title:
            audio = types.FSInputFile("music.mp3")
            await message.answer_audio(audio, caption=f"🎵 {title}")
            os.remove("music.mp3")
        else:
            await message.answer("Hech narsa topilmadi 😔")
    except Exception as e:
        await message.answer("Xatolik yuz berdi. Keyinroq urinib ko'ring.")
    finally:
        await msg.delete()

async def main():
    # Flaskni alohida oqimda ishga tushirish
    Thread(target=run).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
