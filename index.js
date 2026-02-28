const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('VKM Style Bot is Active!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! VKM bot kabi tezkor musiqa qidiruviga xush kelibsiz.\n\nQoʻshiq nomini yozing:'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Qidirilmoqda...');
    
    try {
        // VKM botlar foydalanadigan bazaga o'xshash barqaror API
        const res = await axios.get(`https://api.vkr.llc/music/search?q=${encodeURIComponent(query)}`);
        const songs = res.data.result;

        if (!songs || songs.length === 0) {
            return ctx.editMessageText('😕 Hech narsa topilmadi. Boshqa nom yozib koʻring.');
        }

        const song = songs[0];
        await ctx.editMessageText('📥 Yuklanmoqda...');

        await ctx.replyWithAudio({ url: song.url }, { 
            title: song.title,
            performer: song.artist,
            caption: `✅ @sammusiqalar orqali topildi` 
        });
        
        ctx.deleteMessage(msg.message_id);
    } catch (e) {
        // Agar birinchi baza ishlamasa, zaxira bazaga o'tish
        try {
            const backup = await axios.get(`https://api.deezer.com/search?q=${encodeURIComponent(query)}`);
            const track = backup.data.data[0];
            
            if (track && track.preview) {
                await ctx.replyWithAudio(track.preview, { 
                    title: track.title,
                    performer: track.artist.name,
                    caption: `🎵 Zaxira bazadan topildi.\n✅ @sammusiqalar` 
                });
                return ctx.deleteMessage(msg.message_id);
            }
        } catch (err) {
            console.log(err);
        }
        ctx.editMessageText('⚠️ Hozircha serverda uzilish. Bir ozdan soʻng urinib koʻring.');
    }
});

bot.launch();
