from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd, edit_or_reply


@borg.on(admin_cmd(pattern="ping", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    ed = await edit_or_reply(event, event.from_id, "...")
    start = datetime.now()
    await ed.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await ed.edit("**Pong!**\n`{}` __ms__".format(ms))
