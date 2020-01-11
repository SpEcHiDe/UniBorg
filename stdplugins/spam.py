# For UniBorg
# By Priyam Kalra
# Syntax (.spam <number of msgs [limit = 1000]> <text> )

from asyncio import wait
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types


@borg.on(events.NewMessage(pattern=r"\.spam", outgoing=True))
async def spammer(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        counter = int(message[6:9])
        spam_message = str(e.text[9:])
    for spam in range(counter):
        await e.reply(spam_message)
