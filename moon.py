import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


#config#

bot = Client(
    'sarkilardanindirBot',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

#start mesajı

@bot.on_message(filters.command(['start']))
async def start_(client: Client, message: Message):
    await message.reply_sticker("CAACAgQAAxkBAAI8bmKIvgnlJyCrq9HIxSvCZCbm5CEjAAIaEAACpvFxHg-Z648-SCRWJAQ")
    await message.reply_text(
    f"""● **Selam** {message.from_user.mention}\n\n**» Ben müzik indirme botuyum istediğin müziği indirebilirim**\n\n**✅ Yardım için** /help **komutunu kullanın**""",
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇹🇷 𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾 🇹🇷', url=f'http://t.me/StarSongBot?startgroup=new'),
                  ],[
                    InlineKeyboardButton('✅ 𝖣𝖾𝗌𝗍𝖾𝗄 ', url=f'https://t.me/sarkilardankesitlerimchat{Config.GROUP}'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅 ', url=f'https://t.me/sarkilardankesitlerim{Config.PLAYLIST_NAME}')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 ɢɪᴛʜᴜʙ ᴋᴀʏɴᴀᴋ ᴋᴏᴅᴜ 🧑🏻‍💻', url=f'https://github.com//Song')
                ]
            ]
        )
    )
    
#yardım mesajı

@bot.on_message(filters.command(['help']))
def help(client, message):
    helptext = f'• **Müzik indirmek için /bul komutunu kullabilirsin .**\n\n**Örnek** :\n•> /bul `gece mavisi`'
    message.reply_text(
        text=helptext, 
        quote=False,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('🇹🇷 𝖡𝖾𝗇𝗂 𝖦𝗋𝗎𝖻𝖺 𝖤𝗄𝗅𝖾 🇹🇷', url=f'http://t.me/StarSongBot?startgroup=new'),
                  ],[
                    InlineKeyboardButton('✅ 𝖣𝖾𝗌𝗍𝖾𝗄', url=f'https://t.me/sarkilardankesitlerimchat{Config.GROUP}'),
                    InlineKeyboardButton('⏳ 𝖪𝖺𝗇𝖺𝗅', url=f'https://t.me/sarkilardankesitlerim{Config.PLAYLIST_NAME}')
                  ],[
                    InlineKeyboardButton('🧑🏻‍💻 ɢɪᴛʜᴜʙ ᴋᴀʏɴᴀᴋ ᴋᴏᴅᴜ 🧑🏻‍💻', url=f'https://github.com//Song')
                ]
            ]
        )
    )
#alive mesaji#

@bot.on_message(filters.command("alive") & filters.user(Config.BOT_OWNER))
async def live(client: Client, message: Message):
    livemsg = await message.reply_text('`Merhaba Sahip Bey 🖤`')
    
#musik indirme#

@bot.on_message(filters.command("bul") & ~filters.edited)
def bul(_, message):
    query = " ".join(message.command[1:])
    m = message.reply("<b>• **Şarkı Aranıyor** ...</b>")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]

    except Exception as e:
        m.edit("<b>⛔ **Üzgünüm şarkı bulunamadı.**</b>")
        print(str(e))
        return
    m.edit("<b>•> **İndirme Başladı...**</b>")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"•> [Sahip](https://t.me/akillanmazkral) 𝖳𝖺𝗋𝖺𝖿𝗂𝗇𝖽𝖺𝗇 !"
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        m.edit("•> **Yükleniyor**...")
        message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="@mutsuz_panda")
        m.delete()
        bot.send_audio(chat_id=Config.PLAYLIST_ID, audio=audio_file, caption=rep, performer="@mutsuz_panda", parse_mode='md', title=title, duration=dur, thumb=thumb_name)
    except Exception as e:
        m.edit("<b>⛔ **Hatanın düzelmesini bekleyin** .</b>")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.run()
