const { Telegraf } = require("telegraf");
const yts = require("yt-search");
const ytdl = require("ytdl-core");
const ffmpeg = require("fluent-ffmpeg");
const ffmpegPath = require("ffmpeg-static");
const fs = require("fs");
const express = require("express");

// Render yoki Railway-da bot o'chib qolmasligi uchun kichik server
const app = express();
app.get('/', (req, res) => res.send('Bot is Running!'));
app.listen(process.env.PORT || 8080);

ffmpeg.setFfmpegPath(ffmpegPath);

// Sizning Telegram Tokeningiz
const TOKEN = "8219536583:AAGjX5otvd0kU0xdzhinLuSBvhD6pkHhx2o";
const bot = new Telegraf(TOKEN);

bot.start((ctx) => {
    ctx.reply("🎵 Qo‘shiq nomini yozing — MP3 qilib beraman!");
});

bot.on("text", async (ctx) => {
    try {
        const text = ctx.message.text;
        const msg = await ctx.reply("🔎 Qidirilyapti...");

        const search = await yts(text);

        if (!search.videos.length) {
            return ctx.reply("❌ Qo‘shiq topilmadi");
        }

        const video = search.videos[0];
        // Artist va nomini ajratib olishga harakat qilamiz
        const titleParts = video.title.split('-');
        const performer = titleParts.length > 1 ? titleParts[0].trim() : video.author.name;
        const songName = titleParts.length > 1 ? titleParts[1].trim() : video.title;

        await ctx.editMessageText(`✅ Topildi: ${video.title}\n📥 Yuklanmoqda...`);

        const file = `music_${Date.now()}.mp3`;
        const stream = ytdl(video.url, {
            quality: "highestaudio",
            filter: "audioonly"
        });

        await new Promise((resolve, reject) => {
            ffmpeg(stream)
                .audioBitrate(128)
                .format("mp3")
                .save(file)
                .on("end", resolve)
                .on("error", reject);
        });

        await ctx.replyWithAudio({
            source: fs.createReadStream(file)
        }, {
            title: songName,
            performer: performer,
            caption: `✅ **${performer} - ${songName}**\n📡 @sammusiqalar`,
            parse_mode: 'Markdown'
        });

        // Xabarlarni tozalash
        ctx.deleteMessage(msg.message_id).catch(() => {});
        fs.unlinkSync(file);

    } catch (e) {
        console.log(e);
        ctx.reply("⚠️ YouTube cheklovi yoki xatolik. Iltimos, boshqa nom yozib ko‘ring.");
    }
});

bot.launch();
console.log("🚀 Bot ishlayapti...");
