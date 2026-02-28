import telebot
import requests
import yt_dlp
import os
import threading
from flask import Flask

# Render uchun server
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

# SOZLAMALAR
TOKEN = '8219536583:AAHXIWn25jSv5JdkMLSEIlw2b6_bxAC8fsA'
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 Musiqa nomini yozing, men yuklab beraman!")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    query = message.text
    msg = bot.send_message(message.chat.id, "📥 **Tayyorlanmoqda...**", parse_mode='Markdown')

    def download_process():
        try:
            # 1. YouTube'dan qidirish
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 1, 'type': 'video'}
            r = requests.get(search_url, params=params).json()
            
            if 'items' not in r or not r['items']:
                bot.edit_message_text("😕 Topilmadi.", message.chat.id, msg.message_id)
                return

            v_id = r['items'][0]['id']['videoId']
            url = f"https://www.youtube.com/watch?v={v_id}"
            
            # 2. Yuklash sozlamalari
            file_name = f"music_{message.chat.id}"
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': file_name,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # 3. Yuborish
            full_name = f"{file_name}.mp3"
            if os.path.exists(full_name):
                with open(full_name, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
                os.remove(full_name)
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ FFmpeg xatosi! Render Settings-da Build Command-ni tekshiring.", message.chat.id, msg.message_id)
        
        except Exception as e:
            bot.send_message(message.chat.id, f"⚠️ Xato: {str(e)[:50]}")

    threading.Thread(target=download_process).start()

bot.remove_webhook()
bot.polling(none_stop=True)
