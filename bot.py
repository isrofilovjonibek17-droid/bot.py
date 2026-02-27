import telebot
import yt_dlp
import os

TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
bot = telebot.TeleBot(TOKEN)

def download_audio(url_or_name):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        # YouTube blokidan qochish uchun 'User-Agent'ni yangilaymiz
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    # Agar bu link bo'lmasa, uni qidiruv deb qabul qilamiz
    if not url_or_name.startswith(('http://', 'https://')):
        ydl_opts['default_search'] = 'ytsearch1'
        url_or_name = f"ytsearch1:{url_or_name}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url_or_name, download=True)
        if 'entries' in info:
            data = info['entries'][0]
        else:
            data = info
        
        file_path = ydl.prepare_filename(data).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return file_path, data.get('title', 'Musiqa')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Men endi Instagram va TikTok linklari bilan zo'r ishlayman! 🎵\nLink yuboring yoki qo'shiq nomini yozing.")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    msg = bot.send_message(message.chat.id, "Yuklanmoqda... ⏳")
    try:
        file_path, title = download_audio(message.text)
        
        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✅ {title}")
        
        os.remove(file_path)
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        # Agar YouTube bloklasa, foydalanuvchiga tushunarli xabar beramiz
        bot.edit_message_text("YouTube hozircha blokladi. Iltimos, Instagram yoki TikTok linkini yuboring!", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
