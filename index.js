const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Qoʻshiq nomini yozing, men uni YouTube-siz, tezkor bazalardan topib beraman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Aqlli qidiruv ketyapti...');
    
    try {
        // YouTube-siz ishlaydigan muqobil API
        const response = await axios.get(`https://api-song-downloader.vercel.app/search?q=${encodeURIComponent(query)}`);
        const song = response.data[0];

        if (!song || !song.downloadUrl) {
            return ctx.reply('😕 Kechirasiz, bu qoʻshiq topilmadi.');
        }

        await ctx.replyWithAudio(song.downloadUrl, { 
            caption: `✅ ${song.title}\n🎵 @sammusiqalar` 
        });
        
    } catch (e) {
        ctx.reply('⚠️ Hozircha yuklab boʻlmadi, iltimos boshqa nom yozing.');
    }
});

bot.launch();
