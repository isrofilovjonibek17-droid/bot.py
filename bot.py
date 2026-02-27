import telebot
import yt_dlp
import os

# Bot tokeningiz
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
bot = telebot.TeleBot(TOKEN)

def download_music(query):
    # YouTube blokirovkasidan qochish uchun yangilangan sozlamalar
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'music.%(ext)s',
        'default_search': 'ytsearch1',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        # Blokdan qochish uchun 'user-agent' qo'shamiz
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'quiet': True,
        'no_warnings': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Avval link ekanligini tekshiramiz
            info = ydl.extract_info(query, download=True)
            if 'entries' in info:
                # Agar qidiruv natijasi bo'lsa
                data = info['entries'][0]
            else:
                # Agar to'g'ridan-to'g'ri link bo'lsa
                data = info
            
            file_name = ydl.prepare_filename(data).replace('.webm', '.mp3').replace('.m4a', '.mp3')
            return file_name, data.get('title', 'Musiqa')
        except Exception as e:
            raise e

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Qo'shiq nomini yozing yoki link yuboring (Insta, TikTok, YT). Men srazi topib beraman! 🎵")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    processing_msg = bot.send_message(message.chat.id, "Qidirilmoqda... 🔎")
    try:
        file_path, title = download_music(message.text)
        
        with open(file_path, 'rb') as audio:
            bot.send_audio(
                message.chat.id, 
                audio, 
                caption=f"✅ {title}\n\n@SizningBotiz", 
                title=title
            )
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        bot.delete_message(message.chat.id, processing_msg.message_id)
        
    except Exception as e:
        error_text = str(e)
        if "Sign in to confirm you’re not a bot" in error_text:
            bot.edit_message_text("YouTube meni blokladi. Iltimos, birozdan keyin urinib ko'ring yoki aniqroq link yuboring.", message.chat.id, processing_msg.message_id)
        else:
            bot.edit_message_text(f"Xatolik yuz berdi. Boshqa qo'shiq yozib ko'ring.", message.chat.id, processing_msg.message_id)

bot.polling(none_stop=True)
