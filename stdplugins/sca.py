"""Send Chat Actions
Syntax: .sca <option> <time in sec>
        .scaoptions"""

import asyncio
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="sca (.*) (.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    input_time = event.pattern_match.group(2)
    action = "typing"
    try:
        input_time = int(input_time)
        if (input_time > 0):
            action_time = input_time
            await event.delete()
        async with borg.action(event.chat_id, action):
            await asyncio.sleep(action_time)
    except Exception as e:
        await event.edit("Send in `.sca <option> <time in sec>` format.\nCheck `.scaoptions` for option.")


@borg.on(admin_cmd(pattern="scaoptions"))
async def _(event):
    await event.edit("**Options for sca** \n\n`typing`\n`contact`\n`game`\n`location`\n`voice`\n`round`\n`video`\n`photo`\n`document`\n`cancel`")
