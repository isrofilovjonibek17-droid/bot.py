const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Live!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Musiqa nomini yozing, men uni professional formatda topaman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Qidirilmoqda...');
    
    try {
        const response = await axios.get(`https://saavn.dev/api/search/songs?query=${encodeURIComponent(query)}`);
        
        if (response.data.success && response.data.data.results.length > 0) {
            const song = response.data.data.results[0];
            const downloadUrl = song.downloadUrl[song.downloadUrl.length - 1].url;

            await ctx.replyWithAudio(
                { url: downloadUrl }, 
                { 
                    title: song.name, 
                    performer: song.artists.primary[0].name, 
                    caption: `🎵 **${song.artists.primary[0].name} - ${song.name}**\n\n✅ Toʻliq va sifatli!\n📡 @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            return ctx.deleteMessage(msg.message_id).catch(() => {});
        }
        ctx.reply('😕 Kechirasiz, hech narsa topilmadi.');
    } catch (e) {
        ctx.reply('⚠️ Tarmoqda uzilish boʻldi yoki Node.js xatosi. Qayta urinib koʻring.');
    }
});

bot.launch();
