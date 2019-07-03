"""Emoji

Available Commands:

.emoji shrug

.emoji apple

.emoji :/

.emoji -_-"""

from telethon import events

import asyncio





@borg.on(events.NewMessage(pattern=r"\.(.*)", outgoing=True))

async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2.5

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "hack":

        await event.edit(input_str)

        animation_chars = [
        
            "`Connecting To Hacked Telegram Server...`",
            "`Target Selected.`",
            "`Loading... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Loading... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Loading... 84%\n█████████████████████▒▒▒▒ `",
            "`Loading... 100%\n█████████████████████████ `",
            "`Targeted Account Hacked...\n\nPay 999$ To @r4v4n4 To Remove This Hack`"
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])
