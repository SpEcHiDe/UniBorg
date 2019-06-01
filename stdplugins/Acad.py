# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.Acad", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("Happy Birthday To You")
    await asyncio.sleep(3)
    await event.edit("Happy Birthday To You....")
    await asyncio.sleep(3)
    await event.edit("Happy Birthday Dear Ankit pro ser😉")
    await asyncio.sleep(3)
    await event.edit("Happy Birthday To You")
    await asyncio.sleep(3)
    await event.edit(" 🎉 🎉 🎉 🎉 🎉 🎉 🎉") 
    await asyncio.sleep(3)
    await event.delete()
