const { Telegraf } = require('telegraf');
const ytSearch = require('yt-search');
const ytdl = require('ytdl-core');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is active!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Musiqa nomini yozing, men uni tezda topaman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Tezkor qidiruv...');
    
    try {
        // Faqat bitta natijani qidirish (tezroq bo'ladi)
        const r = await ytSearch({ query, pages: 1 });
        const video = r.videos[0];
        
        if (!video) return ctx.reply('😕 Topilmadi.');

        await ctx.editMessageText('📥 Yuklanmoqda...');

        // Faylni saqlamasdan, to'g'ridan-to'g'ri stream orqali yuborish
        const stream = ytdl(video.url, { 
            filter: 'audioonly', 
            quality: 'highestaudio',
            highWaterMark: 1 << 25 // Bu buferni oshiradi va tezlashtiradi
        });

        await ctx.replyWithAudio({ source: stream, filename: `${video.title}.mp3` }, { 
            caption: `✅ ${video.title}\n@sammusiqalar` 
        });
        
        ctx.deleteMessage(msg.message_id);
    } catch (e) {
        ctx.reply('⚠️ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.');
    }
});

bot.launch();
