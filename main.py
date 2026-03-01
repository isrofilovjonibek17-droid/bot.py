import os
import asyncio
import yt_dlp
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from youtube_search import YoutubeSearch
from flask import Flask
from threading import Thread

# Bot sozlamalari
TOKEN = "8219536583:AAFIAF_XHr9q1yk07rCzpraG7FMfR6loN64"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Render uchun kichik server
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlashda davom etmoqda!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def search_and_download(query):
    results = YoutubeSearch(query, max_results=1).to_dict()
    if not results:
        return None
    
    video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
    file_path = f"{results[0]['id']}.mp3"
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': file_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
        
    return {
        'path': file_path,
        'title': results[0]['title'],
        'duration': results[0]['duration']
    }

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name}! 🎵\nMen musiqa topuvchi botman. Qo'shiq nomini yozing:")

@dp.message(F.text)
async def handle_message(message: types.Message):
    status_msg = await message.answer("Qidirilmoqda... 🔍")
    
    try:
        music_data = search_and_download(message.text)
        if music_data:
            await status_msg.edit_text("Yuklanmoqda... 📥")
            audio_file = types.FSInputFile(music_data['path'])
            
            await message.answer_audio(
                audio_file, 
                caption=f"🎵 {music_data['title']}\n⏱ Davomiyligi: {music_data['duration']}\n@sizning_botingiz",
                title=music_data['title']
            )
            os.remove(music_data['path']) # Faylni o'chirish (joy tejash uchun)
            await status_msg.delete()
        else:
            await status_msg.edit_text("Afsuski, hech narsa topilmadi 😕")
    except Exception as e:
        print(f"Xato: {e}")
        await status_msg.edit_text("Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")

async def main():
    Thread(target=run_flask).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
