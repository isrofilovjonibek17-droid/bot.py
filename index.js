const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Active!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Musiqa nomini yozing, men uni toʻliq va chiroyli formatda topib beraman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Musiqa qidirilmoqda...');
    
    try {
        // Yangi va barqaror musiqa qidiruv API
        const searchUrl = `https://saavn.dev/api/search/songs?query=${encodeURIComponent(query)}`;
        const response = await axios.get(searchUrl);
        
        if (response.data.success && response.data.data.results.length > 0) {
            const song = response.data.data.results[0];
            
            // Eng yuqori sifatli (320kbps) yuklash havolasini olamiz
            const downloadUrl = song.downloadUrl[song.downloadUrl.length - 1].url;

            await ctx.replyWithAudio(
                { url: downloadUrl }, 
                { 
                    title: song.name, 
                    performer: song.artists.primary[0].name, 
                    caption: `🎵 **${song.artists.primary[0].name} - ${song.name}**\n✅ Toʻliq va sifatli!\n📡 @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            return ctx.deleteMessage(msg.message_id).catch(() => {});
        }

        ctx.reply('😕 Kechirasiz, bu qoʻshiq topilmadi. Boshqa nom yozib koʻring.');
    } catch (e) {
        console.log('Xatolik:', e.message);
        ctx.reply('⚠️ Qidiruvda texnik xatolik. Iltimos, bir ozdan soʻng urinib koʻring.');
    }
});

bot.launch();
