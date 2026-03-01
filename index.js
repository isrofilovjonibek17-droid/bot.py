const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('VKM Bot is Running!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! VKM bot kabi tezkor qidiruvga xush kelibsiz.\n\nQoʻshiq nomini yozing:'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Qidirilmoqda...');
    
    try {
        // 1-Bazadan qidirish (Asosiy)
        const res = await axios.get(`https://api.vkr.llc/music/search?q=${encodeURIComponent(query)}`);
        if (res.data.result && res.data.result.length > 0) {
            const song = res.data.result[0];
            await ctx.replyWithAudio({ url: song.url }, { 
                title: song.title,
                performer: song.artist,
                caption: `✅ @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        // 2-Bazadan qidirish (Zaxira)
        const res2 = await axios.get(`https://api.deezer.com/search?q=${encodeURIComponent(query)}`);
        if (res2.data.data && res2.data.data.length > 0) {
            const song = res2.data.data[0];
            await ctx.replyWithAudio(song.preview, { 
                title: song.title,
                performer: song.artist.name,
                caption: `🎵 Deezer'dan topildi.\n✅ @sammusiqalar` 
            });
            return ctx.deleteMessage(msg.message_id);
        }

        ctx.editMessageText('😕 Afsuski, hech qayerdan topilmadi. Boshqa nom yozib koʻring.');
    } catch (e) {
        ctx.editMessageText('⚠️ Serverda vaqtincha uzilish. Iltimos, bir ozdan soʻng urinib koʻring.');
    }
});

bot.launch();
