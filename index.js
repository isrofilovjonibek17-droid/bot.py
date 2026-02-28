const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

// Render serveri o'chib qolmasligi uchun kichik veb-interfeys
const app = express();
app.get('/', (req, res) => res.send('Bot 24/7 rejimida ishlamoqda!'));
app.listen(process.env.PORT || 8080);

// Botingizning tokeni
const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => {
    ctx.reply('🎵 Salom! Men musiqalarni tezkor qidiruvchi aqlli botman.\n\nQoʻshiq nomini yoki xonandani yozing, men uni YouTube-dan emas, toʻgʻridan-toʻgʻri audio bazalardan topaman!');
});

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Aqlli qidiruv boshlandi...');
    
    try {
        // YouTube-ni chetlab o'tuvchi, bir nechta manbalarni birlashtirgan API
        // Bu API musiqalarni ochiq audio bazalardan qidiradi
        const searchUrl = `https://api-music-finder.vercel.app/search?q=${encodeURIComponent(query)}`;
        const response = await axios.get(searchUrl);
        const song = response.data[0]; // Eng yaqin natijani olamiz

        if (!song || !song.downloadUrl) {
            return ctx.editMessageText('😕 Afsuski, bu nom boʻyicha musiqa topilmadi. Boshqacha yozib koʻring.');
        }

        await ctx.editMessageText('✅ Topildi! Yuklanmoqda...');

        // Qo'shiqni yuborish
        await ctx.replyWithAudio(song.downloadUrl, { 
            title: song.title,
            performer: song.artist || 'Musiqa',
            caption: `🎵 **${song.title}**\n\n✅ Muvaffaqiyatli yuklandi!\n📡 Kanalimiz: @sammusiqalar` ,
            parse_mode: 'Markdown'
        });
        
        // "Yuklanmoqda" xabarini o'chirish
        ctx.deleteMessage(msg.message_id);

    } catch (e) {
        console.error('Xato:', e.message);
        ctx.editMessageText('⚠️ Tizimda yuklanish koʻp. Iltimos, 1 daqiqadan soʻng qayta urinib koʻring yoki boshqa nom yozing.');
    }
});

// Bot xato bersa ham to'xtab qolmasligi uchun himoya
bot.catch((err) => {
    console.log('Botda xatolik:', err);
});

bot.launch();

console.log('Bot muvaffaqiyatli ishga tushdi!');
