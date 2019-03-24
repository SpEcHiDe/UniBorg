from telethon import events
import asyncio
import os

@borg.on(events.NewMessage(pattern=r"\.delete (.*)", outgoing=True))
async def handler(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)

	
    if os.path.isfile(input_str):
     os.remove(input_str)
     await event.edit("✅File Deleted 👍🏻")
	 
    else:
         await event.edit("⛔️File Not Found സാധനം കയ്യിലില്ല😬")