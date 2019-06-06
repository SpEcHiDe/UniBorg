# BY @STARKTM1
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.bomb", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
       
 
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(1)
    await event.edit("💣💣💣💣 \n▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(1)
    await event.edit("▪️▪️▪️▪️ \n💣💣💣💣 \n▪️▪️▪️▪️ \n")
    await asyncio.sleep(1)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💣💣💣💣 \n")
    await asyncio.sleep(2)
    await event.edit("▪️▪️▪️▪️ \n▪️▪️▪️▪️ \n💥💥💥💥 \n")
    

    
