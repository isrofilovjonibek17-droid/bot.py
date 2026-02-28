import telebot
import requests
import yt_dlp
import os
import threading
from flask import Flask

# --- RENDER UCHUN KICHIK SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

# --- SOZLAMALAR ---
# Yangi tokeningizni shu yerga joyladim
TOKEN = '8219536583:AAFarvK-7nI4_tYMjTcr9rZ16VeoY713ALk'
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
KANAL_ID = '@sammusiqalar' 
bot = telebot.TeleBot(TOKEN)

# Obuna tekshirish
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(KANAL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 **Musiqa nomini yozing yoki link yuboring!**\n\nMen srazu yuklab beraman.", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, "❗ Botdan foydalanish uchun @sammusiqalar kanaliga obuna bo'ling!")
        return

    query = message.text
    msg = bot.send_message(message.chat.id, "📥 **Tayyorlanmoqda...**", parse_mode='Markdown')

    def download_process():
        try:
            url = ""
            if "http" in query:
                url = query
            else:
                # YouTube'dan birinchi videoni topish
                search_url = "https://www.googleapis.com/youtube/v3/search"
                params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 1, 'type': 'video'}
                data = requests.get(search_url, params=params).json()
                if 'items' in data and len(data['items']) > 0:
                    v_id = data['items'][0]['id']['videoId']
                    url = f"https://www.youtube.com/watch?v={v_id}"
                else:
                    bot.edit_message_text("😕 Topilmadi.", message.chat.id, msg.message_id)
                    return

            # Yuklash sozlamalari
            u_id = str(threading.get_ident())
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': u_id,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}],
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            f_name = f"{u_id}.mp3"
            if os.path.exists(f_name):
                with open(f_name, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
                os.remove(f_name)
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ MP3 tayyorlashda xato.", message.chat.id, msg.message_id)
        except Exception as e:
            bot.send_message(message.chat.id, "❌ Xatolik yuz berdi. Boshqa nom yozib ko'ring.")

    threading.Thread(target=download_process).start()

# Eski ulanishlarni tozalash
bot.remove_webhook()
bot.polling(none_stop=True, skip_pending=True)
