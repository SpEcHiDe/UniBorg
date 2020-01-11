import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from uniborg.util import admin_cmd

deploylink = Config.HEROKU_LINK
repolink = Config.REPO_LINK
packs = Config.PACKS_CONTENT

@borg.on(admin_cmd(pattern="get ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    animation_interval = 0.3
    animation_ttl = range(0, 16)
    input_str = event.pattern_match.group(1)
    if input_str == "repo":
        await event.edit("Click [here](" + repolink + ") to goto the custom github repo.")
    elif input_str == "heroku":
        await event.edit("Click [here](" + deploylink + ") to goto the heroku deploy page.")
    elif input_str == "packs":
        await event.edit(packs)
