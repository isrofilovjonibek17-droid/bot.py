import telebot
import requests
import yt_dlp
import os
import threading
from flask import Flask

# --- RENDER PORT XATOSI UCHUN ---
app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"
def run(): app.run(host='0.0.0.0', port=8080)
threading.Thread(target=run).start()

# --- SOZLAMALAR ---
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
KANAL_ID = '@sammusiqalar' 
bot = telebot.TeleBot(TOKEN)

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
    
    # Agar bu link bo'lsa
    if "http" in query:
        url = query
        msg = bot.send_message(message.chat.id, "📥 **Link aniqlandi. Yuklanmoqda...**", parse_mode='Markdown')
    # Agar bu matn bo'lsa, YouTube'dan eng birinchisini topamiz
    else:
        msg = bot.send_message(message.chat.id, f"🔎 **'{query}' qidirilmoqda va yuklanmoqda...**", parse_mode='Markdown')
        try:
            search_url = "https://www.googleapis.com/youtube/v3/search"
            params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 1, 'type': 'video'}
            data = requests.get(search_url, params=params).json()
            if 'items' in data and len(data['items']) > 0:
                v_id = data['items'][0]['id']['videoId']
                url = f"https://www.youtube.com/watch?v={v_id}"
            else:
                bot.edit_message_text("😕 Hech narsa topilmadi.", message.chat.id, msg.message_id)
                return
        except:
            bot.edit_message_text("⚠️ Qidiruvda xatolik.", message.chat.id, msg.message_id)
            return

    # Yuklash jarayonini boshlash
    threading.Thread(target=download_and_send, args=(url, message.chat.id, msg.message_id)).start()

def download_and_send(url, chat_id, message_id):
    try:
        # Fayl nomi uchun vaqtinchalik nom
        file_id = str(threading.get_ident())
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': file_id,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        filename = f"{file_id}.mp3"
        if os.path.exists(filename):
            with open(filename, 'rb') as audio:
                bot.send_audio(chat_id, audio, caption="✅ @sammusiqalar orqali yuklandi")
            os.remove(filename)
            bot.delete_message(chat_id, message_id)
        else:
            bot.edit_message_text("❌ Yuklashda xato bo'ldi.", chat_id, message_id)
