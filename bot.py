import telebot
import requests
import yt_dlp
import os
from telebot import types

# --- SOZLAMALAR ---
TOKEN = '8219536583:AAGolUIvoSJHbjb9sppjFm__Labw2ZvTNfc'
YOUTUBE_API_KEY = 'AIzaSyCnfj-ygi6RfWfmJ2T0ozKgA-WQ3hv9gz8'
KANAL_ID = '@sammusiqalar' 
KANAL_LINK = 'https://t.me/sammusiqalar'

bot = telebot.TeleBot(TOKEN)

def is_subscribed(user_id):
    try:
        status = bot.get_chat_member(KANAL_ID, user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return True

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f"🌟 **Assalomu aleykum, {message.from_user.first_name}!**\n\n🔍 Qo'shiq nomini yozing:", parse_mode='Markdown')

@bot.message_handler(func=lambda m: True)
def handle_text(message):
    if not is_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Kanalga obuna bo'lish", url=KANAL_LINK))
        bot.send_message(message.chat.id, "❗ **Obuna bo'ling!**", reply_markup=markup, parse_mode='Markdown')
        return

    query = message.text
    msg = bot.send_message(message.chat.id, "🔎 **Qidirilmoqda...**")

    try:
        search_url = "https://www.googleapis.com/youtube/v3/search"
        params = {'part': 'snippet', 'q': query, 'key': YOUTUBE_API_KEY, 'maxResults': 10, 'type': 'video'}
        data = requests.get(search_url, params=params).json()

        if 'items' in data and len(data['items']) > 0:
            markup = types.InlineKeyboardMarkup()
            list_text = f"🎧 **'{query}' bo'yicha natijalar:**\n\n"
            row = []
            for i, item in enumerate(data['items']):
                v_id = item['id']['videoId']
                list_text += f"{i+1}. 🎶 {item['snippet']['title'][:50]}...\n"
                row.append(types.InlineKeyboardButton(f"{i+1}", callback_data=f"dl_{v_id}"))
                if (i + 1) % 5 == 0:
                    markup.row(*row)
                    row = []
            if row: markup.row(*row)
            bot.edit_message_text(list_text, message.chat.id, msg.message_id, reply_markup=markup, parse_mode='Markdown')
        else:
            bot.edit_message_text("😕 Topilmadi.", message.chat.id, msg.message_id)
    except:
        bot.edit_message_text("⚠️ Xatolik.", message.chat.id, msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dl_'))
def download_callback(call):
    v_id = call.data.replace('dl_', '')
    url = f"https://www.youtube.com/watch?v={v_id}"
    bot.edit_message_text("📥 **Yuklanmoqda...**", call.message.chat.id, call.message.message_id)

    try:
        # Render (Linux) uchun FFmpeg avtomatik topiladi
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'%(id)s.%(ext)s',
            'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}],
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = f"{info['id']}.mp3"
        
        with open(filename, 'rb') as audio:
            bot.send_audio(call.message.chat.id, audio, caption="✅ @sammusiqalar")
        
        os.remove(filename)
        bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        bot.send_message(call.message.chat.id, "❌ Xatolik yuz berdi.")

bot.polling(none_stop=True)
