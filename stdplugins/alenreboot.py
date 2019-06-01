# (c) @UniBorg
# Original written by @UniBorg edit by @INF1N17Y

from telethon import events
import asyncio
from collections import deque


@borg.on(events.NewMessage(pattern=r"\.alen", outgoing=True))
async def _(event):
	if event.fwd_from:
		return
	deq = deque(list("ALEN"))
	for _ in range(21):
		await asyncio.sleep(0.1)
		await event.edit("".join(deq))
		deq.rotate(3)
    
