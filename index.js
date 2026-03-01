const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot is Live!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Musiqani nomi yoki xonandasi bilan yozing, men uni professional formatda topaman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Qidirilmoqda...');
    
    try {
        // Dunyo bo'yicha eng barqaror musiqa API
        const response = await axios.get(`https://saavn.dev/api/search/songs?query=${encodeURIComponent(query)}`);
        
        if (response.data.success && response.data.data.results.length > 0) {
            const song = response.data.data.results[0];
            
            // Eng yuqori sifatli audio havolasini tanlash
            const downloadUrl = song.downloadUrl[song.downloadUrl.length - 1].url;

            // "Yuklanmoqda" deb xabarni yangilash (xatosiz)
            try { await ctx.editMessageText('📤 Yuklanmoqda...'); } catch (e) {}

            await ctx.replyWithAudio(
                { url: downloadUrl }, 
                { 
                    title: song.name, // Qo'shiq nomi
                    performer: song.artists.primary[0].name, // Artist nomi
                    caption: `🎵 **${song.artists.primary[0].name} - ${song.name}**\n\n✅ Toʻliq va sifatli!\n📡 @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            
            return ctx.deleteMessage(msg.message_id).catch(() => {});
        }

        ctx.reply('😕 Kechirasiz, bunday qoʻshiq topilmadi. Iltimos, boshqa nom yozib koʻring.');
    } catch (e) {
        console.log('Xato:', e.message);
        ctx.reply('⚠️ Tarmoqda uzilish boʻldi. Iltimos, bir ozdan soʻng qayta urinib koʻring.');
    }
});

bot.launch();
