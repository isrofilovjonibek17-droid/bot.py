import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import yt_dlp
from youtube_search import YoutubeSearch
from flask import Flask
from threading import Thread

# --- TOKEN SHU YERDA ---
TOKEN = "8219536583:AAH0SvNG4ES94u0SIfFa6ibszIxjWeGBF-c"
bot = Bot(token=TOKEN)
dp = Dispatcher()

app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Assalomu alaykum! Musiqa nomini yozing, men topib beraman. 🎵")

@dp.message()
async def search_and_send(message: types.Message):
    query = message.text
    if not query: return
    
    wait_msg = await message.answer("Qidirilmoqda... 🔎")
    
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        if not results:
            await wait_msg.edit_text("Hech narsa topilmadi. 😔")
            return

        video_url = f"https://www.youtube.com{results[0]['url_suffix']}"
        file_path = f"audio_{message.from_user.id}.mp3"

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_path.replace('.mp3', ''),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
        
        # To'g'ri fayl nomini topish (ba'zan .mp3 avtomat qo'shiladi)
        actual_file = file_path if os.path.exists(file_path) else f"{file_path}.mp3"

        audio = types.FSInputFile(actual_file)
        await bot.send_audio(chat_id=message.chat.id, audio=audio, caption=f"✅ {results[0]['title']}")
        
        if os.path.exists(actual_file): os.remove(actual_file)
        await wait_msg.delete()

    except Exception as e:
        await wait_msg.edit_text(f"Xatolik: {str(e)}")

async def main():
    Thread(target=run_flask).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
