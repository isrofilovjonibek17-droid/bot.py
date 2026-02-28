import telebot
import requests
import yt_dlp
import os
import threading
from flask import Flask

# --- RENDER UCHUN PORT SCAN MUAMMOSINI YECHISH (FLASK) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is running!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

# --- SOZLAMALAR (TOKENLARINGIZ) ---
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
KANAL_ID = '@sammusiqalar' 
bot = telebot.TeleBot(TOKEN)

# Obuna tekshirish funksiyasi
def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(KANAL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return True

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 **Salom! Musiqa nomini yozing yoki link yuboring.**\n\nMen uni darhol MP3 qilib beraman!", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    if not is_subscribed(message.from_user.id):
        bot.send_message(message.chat.id, f"❗ Botdan foydalanish uchun {KANAL_ID} kanaliga obuna bo'ling!")
        return

    query = message.text
    msg = bot.send_message(message.chat.id, "📥 **Tayyorlanmoqda...**", parse_mode='Markdown')

    def download_job():
        try:
            url = ""
            if "http" in query:
                url = query
            else:
                # YouTube'dan eng birinchi videoni qidirish
                search_url = "https://www.googleapis.com/youtube/v3/search"
                params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 1, 'type': 'video'}
                data = requests.get(search_url, params=params).json()
                if 'items' in data and len(data['items']) > 0:
                    v_id = data['items'][0]['id']['videoId']
                    url = f"https://www.youtube.com/watch?v={v_id}"
                else:
                    bot.edit_message_text("😕 Hech narsa topilmadi.", message.chat.id, msg.message_id)
                    return

            # Yuklash va MP3 qilish sozlamalari
            unique_name = str(threading.get_ident())
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': unique_name,
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            audio_file = f"{unique_name}.mp3"
            if os.path.exists(audio_file):
                with open(audio_file, 'rb') as audio:
                    bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
                os.remove(audio_file)
                bot.delete_message(message.chat.id, msg.message_id)
            else:
                bot.edit_message_text("❌ Yuklashda xatolik yuz berdi.", message.chat.id, msg.message_id)

        except Exception as e:
            bot.send_message(message.chat.id, "❌ Bu qo'shiqni yuklab bo'lmadi. Iltimos, nomini to'g'ri yozing.")

    # Render o'chib qolmasligi uchun yuklashni alohida oqimda bajaramiz
    threading.Thread(target=download_job).start()

bot.polling(none_stop=True)
