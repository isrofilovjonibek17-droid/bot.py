const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Bot Online!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Qoʻshiq yoki xonanda nomini yozing:'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔍 Qidirilmoqda...');
    
    try {
        // Barqaror musiqa bazasi (Artist va Title bilan qaytaradi)
        const res = await axios.get(`https://api.vkr.llc/music/search?q=${encodeURIComponent(query)}`);
        
        if (res.data.result && res.data.result.length > 0) {
            // To'liq qo'shiqni (60 sekdan uzun) tanlash
            const song = res.data.result.find(s => s.duration > 60) || res.data.result[0];

            // Xabarni tahrirlashda xato bermasligi uchun try-catch ichiga olamiz
            try { await ctx.editMessageText('📥 Yuklanmoqda...'); } catch (e) {}

            await ctx.replyWithAudio(
                { url: song.url }, 
                { 
                    title: song.title, 
                    performer: song.artist, 
                    caption: `🎵 **${song.artist} - ${song.title}**\n✅ @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            
            // "Yuklanmoqda" xabarini o'chirish
            return ctx.deleteMessage(msg.message_id).catch(() => {});
        }

        ctx.reply('😕 Hech narsa topilmadi. Boshqa nom yozib koʻring.');
    } catch (e) {
        console.log('Xatolik:', e.message);
        ctx.reply('⚠️ Hozircha bu qoʻshiqni topib boʻlmadi. Iltimos, keyinroq urinib koʻring.');
    }
});

// Bot o'chib qolmasligi uchun global xatoliklarni ushlash
process.on('uncaughtException', (err) => console.log('Kritik xato:', err));

bot.launch();
