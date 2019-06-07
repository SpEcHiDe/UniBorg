# By STARKTM1
from telethon import events
import asyncio
import os
import sys


@client.on(events.NewMessage(outgoing=True, pattern=r'\.save'))
async def handler(event):
    if event.is_reply:
        replied = await event.get_reply_message()
        sender = replied.sender_id
        await client.download_profile_photo(sender)
        await event.respond('Saved your photo {}'.format(sender.username))
