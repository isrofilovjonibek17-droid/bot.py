import telebot
import requests
import yt_dlp
import os
import threading
from flask import Flask

# --- RENDER UCHUN SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is live!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

# --- SOZLAMALAR ---
TOKEN = '8219536583:AAHXIWn25jSv5JdkMLSEIlw2b6_bxAC8fsA' 
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 **Musiqa nomini yozing!**\n\nMen uni qidirib, MP3 formatida yuboraman.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    query = message.text
    msg = bot.send_message(message.chat.id, "📥 **Qidirilmoqda...**")

    def download_process():
        try:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 1, 'type': 'video'}
            data = requests.get(search_url, params=params).json()
            
            if 'items' not in data or not data['items']:
                bot.edit_message_text("😕 Hech narsa topilmadi.", message.chat.id, msg.message_id)
                return

            v_id = data['items'][0]['id']['videoId']
            url = f"https://www.youtube.com/watch?v={v_id}"
            
            u_id = str(threading.get_ident())
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': u_id,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}],
                'quiet': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            f_name = f"{u_id}.mp3"
            if os.path.exists(f_name):
                with open(f_name, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
                os.remove
