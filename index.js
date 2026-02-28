const { Telegraf } = require('telegraf');
const ytSearch = require('yt-search');
const ytdl = require('ytdl-core');
const express = require('express');
const fs = require('fs');

// Render uchun server
const app = express();
app.get('/', (req, res) => res.send('Bot ishlayapti!'));
app.listen(process.env.PORT || 8080);

// YANGI TOKEN SHU YERDA:
const bot = new Telegraf('8219536583:AAEOacmJ-EeP0ryMZuaPMJSocQRUzHwJofQ');

bot.start((ctx) => ctx.reply('🎵 Musiqa nomini yozing, men uni yuklab beraman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Qidirilmoqda...');

    try {
        const r = await ytSearch(query);
        const video = r.videos[0];

        if (!video) {
            return ctx.editMessageText('😕 Hech narsa topilmadi.');
        }

        const fileName = `${ctx.chat.id}.mp3`;
        
        ytdl(video.url, { filter: 'audioonly', quality: 'highestaudio' })
            .pipe(fs.createWriteStream(fileName))
            .on('finish', async () => {
                await ctx.replyWithAudio({ source: fileName }, { caption: `✅ ${video.title}\n@sammusiqalar` });
                if (fs.existsSync(fileName)) fs.unlinkSync(fileName);
                ctx.deleteMessage(msg.message_id);
            });

    } catch (e) {
        ctx.reply('⚠️ Xatolik! Iltimos, boshqa nom yozib ko\'ring.');
    }
});

bot.launch();
