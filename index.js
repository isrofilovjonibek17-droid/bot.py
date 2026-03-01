const { Telegraf } = require('telegraf');
const axios = require('axios');
const express = require('express');

const app = express();
app.get('/', (req, res) => res.send('Music Bot is ready!'));
app.listen(process.env.PORT || 8080);

const bot = new Telegraf('8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o');

bot.start((ctx) => ctx.reply('🎵 Salom! Musiqa nomini yozing, men uni barcha ma’lumotlari bilan topib beraman!'));

bot.on('text', async (ctx) => {
    const query = ctx.message.text;
    const msg = await ctx.reply('🔎 Qidirilmoqda...');
    
    try {
        // Asosiy va eng sifatli baza
        const res = await axios.get(`https://api.vkr.llc/music/search?q=${encodeURIComponent(query)}`);
        
        if (res.data.result && res.data.result.length > 0) {
            // Davomiyligi 60 soniyadan ko'p bo'lgan birinchi to'liq qo'shiqni olish
            const song = res.data.result.find(s => s.duration > 60) || res.data.result[0];

            await ctx.replyWithAudio(
                { url: song.url }, 
                { 
                    title: song.title, // Qo'shiq nomi
                    performer: song.artist, // Artist nomi
                    caption: `✅ **${song.artist} - ${song.title}**\n📡 @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            return ctx.deleteMessage(msg.message_id);
        }

        // Agar yuqoridagidan topilmasa, Deezer bazasidan artist nomi bilan qidirish
        const res2 = await axios.get(`https://api.deezer.com/search?q=${encodeURIComponent(query)}`);
        if (res2.data.data && res2.data.data.length > 0) {
            const song2 = res2.data.data[0];
            
            await ctx.replyWithAudio(
                { url: song2.preview }, // Preview bo'lsa ham artist nomi bilan chiqadi
                { 
                    title: song2.title,
                    performer: song2.artist.name,
                    caption: `🎵 **${song2.artist.name} - ${song2.title}**\n✅ @sammusiqalar`,
                    parse_mode: 'Markdown'
                }
            );
            return ctx.deleteMessage(msg.message_id);
        }

        ctx.editMessageText('😕 Kechirasiz, hech qanday ma’lumot topilmadi.');
    } catch (e) {
        ctx.editMessageText('⚠️ Qidiruvda xatolik yuz berdi. Iltimos, qaytadan urinib koʻring.');
    }
});

bot.launch();
