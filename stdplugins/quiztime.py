from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.quiz1", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("Question 1")
    await asyncio.sleep(2)
    await event.edit("Who Was The Head of Shield")
    await asyncio.sleep(2)
    await event.edit("Who Was The Head of Shield \nTime 20sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 19sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 18sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 17sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 16sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 15sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 14sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 13sec") 
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 12sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 11sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 10sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 09sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 08sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 07sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 06sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 05sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 04sec"
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 03sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 02sec")
    await asyncio.sleep(1)
    await event.edit("Who Was The Head of Shield \nTime 01sec")
    await asyncio.sleep(1)
    await event.edit("Ok Time Up Plox......✌️ \nThe Answer Is Alexander Pierce")

