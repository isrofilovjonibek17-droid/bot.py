import telebot, yt_dlp, os, threading, requests
from flask import Flask
from static_ffmpeg import add_paths

add_paths()

app = Flask('')
@app.route('/')
def home(): return "Bot is live!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

TOKEN = '8219536583:AAHXIWn25jSv5JdkMLSEIlw2b6_bxAC8fsA' 
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda m: True)
def download(message):
    msg = bot.send_message(message.chat.id, "📥 **Qidirilmoqda...**")
    try:
        # YouTube API orqali qidirish
        search_url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={message.text}&key={YOUTUBE_API_KEY}&maxResults=1&type=video"
        r = requests.get(search_url).json()
        
        if 'items' not in r or not r['items']:
            bot.edit_message_text("😕 Hech narsa topilmadi.", message.chat.id, msg.message_id)
            return

        v_id = r['items'][0]['id']['videoId']
        url = f"https://www.youtube.com/watch?v={v_id}"
        u_id = str(message.chat.id)
        
        # BLOKDAN O'TISH UCHUN SOZLAMALAR
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': u_id,
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}],
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0', # IPv4 ishlatish
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open(f"{u_id}.mp3", 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
        
        os.remove(f"{u_id}.mp3")
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"⚠️ Xatolik! Iltimos, boshqa nom yozib ko'ring.", message.chat.id, msg.message_id)
        print(f"Error: {e}")

bot.remove_webhook()
bot.polling(none_stop=True)
