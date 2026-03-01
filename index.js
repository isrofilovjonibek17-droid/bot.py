const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Full Music Bot is Running!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Men toʻliq hajmdagi musiqalarni qidiruvchi botman.\n\nQoʻshiq nomini yozing:'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Toʻliq musiqalar bazasidan qidirilmoqda...');
    
    try {
        // 1-Bazadan qidirish (To'liq MP3 bazasi)
        const searchUrl = `https://meow-music-api.vercel.app/search?q=${encodeURIComponent(query)}`;
        const res = await axios.get(searchUrl);
        const song = res.data[0];

        if (song && song.url) {
            await ctx.replyWithAudio(song.url, { 
                title: song.title,
                performer: song.artist,
                caption: `✅ Toʻliq talqin\n📡 @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        // 2-Baza (Agar birinchisi topmasa)
        const res2 = await axios.get(`https://api.vkr.llc/music/search?q=${encodeURIComponent(query)}`);
        if (res2.data.result && res2.data.result.length > 0) {
            const song2 = res2.data.result[0];
            await ctx.replyWithAudio(song2.url, { 
                title: song2.title,
                performer: song2.artist,
                caption: `✅ Topildi!\n📡 @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        ctx.editMessageText('😕 Toʻliq variant topilmadi. Iltimos, boshqacha yozib koʻring.');
    } catch (e) {
        ctx.editMessageText('⚠️ Server band. Bir ozdan soʻng qayta urinib koʻring.');
    }
});

bot.launch();
