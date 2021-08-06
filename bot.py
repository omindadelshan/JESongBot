#    Copyright (C) 2021 - Infinity Bots
#    This programme is a part of Infinity Bots
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import logging
import requests
import aiohttp
import youtube_dl
from pyrogram import filters, Client, idle
from youtube_search import YoutubeSearch
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import API_ID, API_HASH, BOT_TOKEN

# logging
bot = Client(
   "Song Downloader",
   api_id=API_ID,
   api_hash=API_HASH,
   bot_token=BOT_TOKEN,
)


@bot.on_message(filters.command("start") & ~filters.edited)
async def start(_, message):
   if message.chat.type == 'private':
       await message.reply("**🔥Hey There,𝐈 𝐀𝐦 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥𝐥 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐒𝐨𝐧𝐠 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭...🔥.𝐌𝐚𝐝𝐞 𝐁𝐲 𝐎𝐦𝐢𝐧𝐝𝐚...🔥🔥😋
                           "🤖🔥 𝗛𝗼𝘄 𝗧𝗼 𝗨𝘀𝗲 𝗠𝗲 𝗘𝘅𝗮𝗺𝗽𝗹𝗲 👉👉 /song [song name]`",
                           "ℙ𝕠𝕨𝕖𝕣𝕕 𝔹𝕪 💠@sdprojectupdates / @omindas...😋"
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "🔥𝙳𝚎𝚟𝚎𝚕𝚘𝚙𝚎𝚛🔥", url="https://t.me/omindas"),
                                        InlineKeyboardButton(
                                            "🤖 𝚄𝚙𝚍𝚊𝚝𝚎 𝙲𝚑𝚊𝚗𝚗𝚊𝚕", url="https://t.me/sdprojectupdates"),
                                        InlineKeyboardButton(
                                            "💠 𝚂𝚘𝚞𝚛𝚌𝚎 𝙲𝚘𝚍𝚎 💠", url="https://github.com/omindadelsha"),
                                        InlineKeyboardButton(
                                            "✳️ 𝙾𝚞𝚛 𝙼𝚘𝚛𝚎 𝚋𝚘𝚝𝚜✳️", url=https://t.me/BotFather"),
                                    ]]
                            ))
   else:
      await message.reply("**Song downloader bot is online ✨**")


@bot.on_message(filters.command("song") & ~filters.edited)
async def song(_, message):
    if len(message.command) < 2:
       return await message.reply("**Usage:**\n - `/song [query]`")
    query = message.text.split(None, 1)[1]
    shed = await message.reply("🔎 𝐒𝐞𝐚𝐫𝐜𝐡𝐢𝐧𝐠 𝐒𝐨𝐧𝐠 🔎")
    ydl_opts = {
       "format": "bestaudio[ext=m4a]",
       "geo-bypass": True,
       "nocheckcertificate": True,
       "outtmpl": "downloads/%(id)s.%(ext)s",
       }
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)

        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]
        channel = results[0]["channel"]
    except Exception as e:
        await shed.edit(
            "❌ Found Nothing.\n\nTry another keywork or maybe spell it properly."
        )
        print(str(e))
        return
    await shed.edit("📩 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐬𝐨𝐧𝐠 📩")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = "✓@𝐨𝐦𝐢𝐧𝐝𝐚𝐬✓"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await shed.edit("📤𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠 𝐒𝐨𝐧𝐠 𝐁𝐲 𝐎𝐦𝐢𝐧𝐝𝐚📤")
        s = await message.reply_audio(audio_file, caption=rep, thumb=thumb_name, parse_mode='md', title=title, duration=dur, performer=channel)
        await shed.delete()
    except Exception as e:
        await shed.edit("❌ Error")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

bot.start()
idle()
