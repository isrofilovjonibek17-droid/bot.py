import telebot
import yt_dlp
import os

# Bot tokeningiz allaqachon kodingizda bor, uni o'zgartirmang
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
bot = telebot.TeleBot(TOKEN)

def download_audio(query, is_url=True):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    if not is_url:
        ydl_opts['default_search'] = 'ytsearch'
        query = f"ytsearch1:{query}"

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        if 'entries' in info:
            filename = ydl.prepare_filename(info['entries'][0]).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        else:
            filename = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        return filename

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Salom! Menga qo'shiq nomini yozing yoki Instagram, TikTok, YouTube linkini yuboring. Men sizga musiqasini topib beraman! 🎵")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    msg = bot.send_message(message.chat.id, "Qidirilmoqda... Bir oz kuting ⏳")
    try:
        is_url = message.text.startswith(('http://', 'https://'))
        file_path = download_audio(message.text, is_url=is_url)
        
        with open('music.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio)
        
        os.remove('music.mp3') 
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"Xatolik: Topilmadi yoki link xato. Qayta urinib ko'ring.", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
