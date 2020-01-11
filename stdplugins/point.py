# For UniBorg
# By Priyam Kalra
# Syntax (.point <text_to_print>)
from telethon import events
from uniborg.util import admin_cmd
import asyncio
from telethon.tl import functions, types

@borg.on(admin_cmd(pattern="point ?(.*)"))
async def _(event):
        if event.fwd_from:
            return
        input = event.pattern_match.group(1)
        await event.edit("╱╭━━┳━┳━┳╮" + " " + input + "\n━┫╱┓┣┳━━━╯\n╱╱╱┃┃╯\n━┫╱╰┛╯\n╱╰━━━╯\n")
