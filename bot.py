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
       await message.reply("**🔥Hey There,𝐈 𝐀𝐦 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥𝐥 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦 𝐒𝐨𝐧𝐠 𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐞𝐫 𝐁𝐨𝐭.🇱🇰 𝚈𝚘𝚞 𝙲𝚊𝚗 𝚍𝚘𝚠𝚗𝚕𝚘𝚊𝚍 𝚜𝚘𝚗𝚐 𝚒𝚜 𝚜𝚞𝚙𝚎𝚛 𝚚𝚞𝚊𝚕𝚒𝚝𝚢🔰.👨‍💻 𝑀𝑦 𝑀𝑎𝑠𝑡𝑒𝑟 𝐼𝑠 𝑂𝑚𝑖𝑛𝑑𝑎 👨‍💻. 💓𝑻𝒉𝒊𝒔 𝑩𝒐𝒕 𝒑𝒐𝒘𝒆𝒓𝒅 𝒃𝒚 @sdprojectupdates 🔥.\nUsage:** `/song [song name]`",   
                            reply_markup=InlineKeyboardMarkup(
                                [[
                                        InlineKeyboardButton(
                                            "💥Dev💥", url="https://t.me/omindas"),
                                        InlineKeyboardButton(
                                            "🔰channal🔰", url="https://t.me/sdprojectupdates")
                                    ]]
                            ))
   else:
      await message.reply("**Song downloader bot is online ✨**")


@bot.on_message(filters.command("song") & ~filters.edited)
async def song(_, message):
    if len(message.command) < 2:
       return await message.reply("**Usage:**\n - `/song [query]`")
    query = message.text.split(None, 1)[1]
    shed = await message.reply("🔎 Finding the song 🔎")
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
    await shed.edit("📥 Downloading 📤")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = "@sdprojectupddates"
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        await shed.edit("📤 Uploading Ominda 📤")
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
