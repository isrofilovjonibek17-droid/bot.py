import telebot
import yt_dlp
import os

# Botingiz TOKЕNi
bot = telebot.TeleBot('8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc')

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "Salom! Menga YouTube, Instagram yoki TikTok linkini yuboring, men uni sizga MP3 qilib beraman! 🎵")

@bot.message_handler(func=lambda message: True)
def download_music(message):
    url = message.text
    if any(site in url for site in ['youtube.com', 'youtu.be', 'instagram.com', 'tiktok.com']):
        msg = bot.send_message(message.chat.id, "Yuklanmoqda... ⏳")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'music.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('music.mp3', 'rb') as audio:
                bot.send_audio(message.chat.id, audio, caption="Tayyor! ✅")
            
            os.remove('music.mp3')
            bot.delete_message(message.chat.id, msg.message_id)
        except Exception as e:
            bot.edit_message_text("Xatolik yuz berdi. Linkni tekshiring.", message.chat.id, msg.message_id)
    else:
        bot.reply_to(message, "Iltimos, faqat video linkini yuboring.")

bot.infinity_polling()
