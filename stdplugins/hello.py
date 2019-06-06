# By @STARKTM1
from telethon import events
import asyncio
import os
import sys


@borg.on(events.NewMessage(pattern=r"\.hello", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
        
        
    await event.edit("╔┓┏╦━━╦┓╔┓╔━━╗\
                      ║┗┛║┗━╣┃║┃║╯╰║\
                      ║┏┓║┏━╣┗╣┗╣╰╯║\
                      ╚┛┗╩━━╩━╩━╩━━╝")
