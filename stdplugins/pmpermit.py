"""Personal Message Spammer
Available Commands:
"""
import asyncio
import json
from telethon import events
from telethon.tl import functions, types

borg.storage.PM_WARNS = {}

borg.storage.ACCEPTED_USERS = []

@borg.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def monito_p_m_s(event):
    sender = await event.get_sender()
    if Config.NO_P_M_SPAM and not sender.bot:
        chat = await event.get_chat()
        if chat.id not in borg.storage.ACCEPTED_USERS and chat.id != borg.uid:
            if chat.id not in borg.storage.PM_WARNS:
                borg.storage.PM_WARNS.update({chat.id: 0})
            if borg.storage.PM_WARNS[chat.id] == Config.MAX_FLOOD_IN_P_M_s:
                r = await event.reply(
                    "I am currently offline. Please do not SPAM me."
                )
                await asyncio.sleep(3)
                await borg(functions.contacts.BlockRequest(chat.id))
                await r.delete()
                return
            r = await event.reply(
                "Hi! I will answer to your message soon. Please wait for my response and don't spam my PM. Thanks"
            )
            borg.storage.PM_WARNS[chat.id] += 1
            await asyncio.sleep(3)
            await r.delete()


@borg.on(events.NewMessage(pattern=r"\.approve ?(.*)", outgoing=True))
async def approve_p_m(event):
    if event.fwd_from:
        return
    reason = event.pattern_match.group(1)
    chat = await event.get_chat()
    if Config.NO_P_M_SPAM:
        if event.is_private:
            if chat.id not in borg.storage.ACCEPTED_USERS:
                if chat.id in borg.storage.PM_WARNS:
                    del borg.storage.PM_WARNS[chat.id]
                borg.storage.ACCEPTED_USERS.append(chat.id)
                await event.edit("Private Message Accepted")
                await asyncio.sleep(3)
                await event.delete()


@borg.on(events.NewMessage(pattern=r"\.list approved pms", outgoing=True))
async def approve_p_m(event):
    if event.fwd_from:
        return
    await event.edit(json.dumps(borg.storage.ACCEPTED_USERS, sort_keys=True, indent=4))
