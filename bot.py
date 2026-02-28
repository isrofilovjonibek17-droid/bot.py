import telebot, yt_dlp, os, threading, requests
from flask import Flask
from static_ffmpeg import add_paths

# FFmpeg yo'lini qo'shish
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
        r = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={message.text}&key={YOUTUBE_API_KEY}&maxResults=1&type=video").json()
        v_id = r['items'][0]['id']['videoId']
        url = f"https://www.youtube.com/watch?v={v_id}"
        u_id = str(message.chat.id)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': u_id,
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '128'}],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        with open(f"{u_id}.mp3", 'rb') as audio:
            bot.send_audio(message.chat.id, audio, caption="✅ @sammusiqalar")
        os.remove(f"{u_id}.mp3")
        bot.delete_message(message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ Xato: {str(e)}", message.chat.id, msg.message_id)

bot.remove_webhook()
bot.polling(none_stop=True)
