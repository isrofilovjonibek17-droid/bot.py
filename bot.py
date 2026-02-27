import telebot
import yt_dlp
import os

# Bot tokeningizni o'zgartirmang, u rasmda ko'ringanidek qolsin
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
bot = telebot.TeleBot(TOKEN)

def download_music(query):
    # Yuklash sozlamalari
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'default_search': 'ytsearch1', # YouTube'dan 1-chi natijani qidirish
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True, # Ortiqcha yozuvlarni terminalda chiqarmaslik
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(query, download=True)
        # Fayl nomini olish
        file_name = ydl.prepare_filename(info['entries'][0]).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        title = info['entries'][0]['title']
        return file_name, title

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Menga qo'shiq nomini yozing, men darhol topib beraman! 🎵")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    msg = bot.send_message(message.chat.id, "Qidirilmoqda... 🔎")
    try:
        file_path, title = download_music(message.text)
        
        with open(file_path, 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption=f"✅ Topildi: {title}")
        
        # Serverda joy egallamasligi uchun faylni o'chiramiz
        os.remove(file_path)
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"Kechirasiz, qo'shiq topilmadi: {str(e)}", message.chat.id, msg.message_id)

bot.polling(none_stop=True)
