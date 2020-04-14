"""
command: .singer singer name - song name 
by @quiec
"""
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from PyLyrics import *

@borg.on(admin_cmd(pattern="singer (.*)"))
async def _(event):
    if event.fwd_from:
        return
    i = 0

    input_str = event.pattern_match.group(1)
    
    try:
        song = input_str.split("-")
        if len(song) == 1:
            await event.edit("Usage: .singer Duman - Haberin Yok Ölüyorum")
        else:
            await event.edit("🔍︎Searching lyrics")
            lycirs = PyLyrics.getLyrics(song[0].strip(), song[1].strip()).split("\n")
            await event.edit(f"Singing {song[0].strip()} from {song[1].strip()} 🎙")
            while i < len(lycirs):
                await asyncio.sleep(2)
                await event.edit(lycirs[i])
                i += 1
    except ValueError:
        await event.edit("Song not found")

