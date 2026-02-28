const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot ishlayapti!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Musiqa nomini yozing, men darhol topaman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Qidirilmoqda...');
    
    try {
        // YouTube API o'rniga ochiq qidiruv API dan foydalanamiz
        const searchUrl = `https://musiqa-api.vercel.app/search?q=${encodeURIComponent(query)}`;
        const response = await axios.get(searchUrl);
        const song = response.data[0];

        if (!song) return ctx.reply('😕 Topilmadi.');

        await ctx.editMessageText('📥 Yuklanmoqda...');

        await ctx.replyWithAudio(song.downloadUrl, { 
            caption: `✅ ${song.title}\n🎵 @sammusiqalar` 
        });
        
        ctx.deleteMessage(msg.message_id);
    } catch (e) {
        console.error(e);
        ctx.reply('⚠️ Hozircha bu qoʻshiqni yuklab boʻlmadi. Boshqa nom yozib koʻring.');
    }
});

bot.launch();
