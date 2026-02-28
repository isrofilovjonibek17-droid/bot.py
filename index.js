const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot 100% Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Musiqa nomini yozing, men uni bir nechta bazalardan qidirib topaman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Bir nechta manbadan qidirilmoqda...');
    
    try {
        // 1-manba (Zaxira API)
        const response = await axios.get(`https://music-api-v2.vercel.app/search?q=${encodeURIComponent(query)}`);
        const song = response.data[0];

        if (song && song.downloadUrl) {
            await ctx.replyWithAudio(song.downloadUrl, { 
                caption: `✅ ${song.title}\n🎵 @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        // Agar 1-manbadan topilmasa, 2-manbani tekshiradi
        const altResponse = await axios.get(`https://shazam-api-free.vercel.app/download?q=${encodeURIComponent(query)}`);
        if (altResponse.data.url) {
            await ctx.replyWithAudio(altResponse.data.url, { 
                caption: `✅ Topildi!\n🎵 @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        ctx.reply('😕 Afsuski, hamma manbalarda ham bu qoʻshiq topilmadi. Boshqa xonandani yozib koʻring.');
    } catch (e) {
        ctx.reply('⚠️ Tarmoqda yuklanish. Iltimos, bir ozdan soʻng qayta urinib koʻring.');
    }
});

bot.launch();
