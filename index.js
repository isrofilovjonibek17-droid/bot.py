const { Telegraf } = require('telegraf');
const ytSearch = require('yt-search');
const ytdl = require('@distube/ytdl-core');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Musiqa nomini yozing!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Qidirilmoqda...');
    
    try {
        const r = await ytSearch({ query, pages: 1 });
        const video = r.videos[0];
        
        if (!video) return ctx.reply('😕 Hech narsa topilmadi.');

        await ctx.editMessageText('📥 Yuklanmoqda...');

        const stream = ytdl(video.url, { 
            filter: 'audioonly', 
            quality: 'highestaudio',
            highWaterMark: 1 << 25 
        });

        await ctx.replyWithAudio({ source: stream, filename: `${video.title}.mp3` }, { 
            caption: `✅ ${video.title}\n🎵 @sammusiqalar` 
        });
        
        ctx.deleteMessage(msg.message_id);
    } catch (e) {
        console.error(e);
        ctx.reply('⚠️ YouTube cheklovi yoki xatolik. Iltimos, boshqa nom yozib koʻring.');
    }
});

// Xatolik bo'lsa bot o'chib qolmasligi uchun
bot.catch((err) => console.error('Bot Error:', err));
bot.launch();
