# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Theid file is stolen from https://github.com/udf/uniborg/blob/kate/stdplugins/info.py
"""Get Detailed info about any message
Syntax: .yaml"""
from telethon import events
import io
from uniborg.util import admin_cmd, parse_pre, yaml_format


@borg.on(admin_cmd(pattern="yaml"))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        event = await event.get_reply_message()
    the_real_message = yaml_format(event)
    if len(the_real_message) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(the_real_message)) as out_file:
            out_file.name = "yaml.html"
            await event.reply(
                file=out_file,
                force_document=True,
            )
            # await event.delete()
    else:
        await event.reply(
            the_real_message,
            parse_mode=parse_pre
        )
