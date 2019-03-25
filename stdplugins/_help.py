from telethon import events, functions, __version__
import sys


@borg.on(events.NewMessage(pattern=r"\.helpme", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    help_string = """I AM LEGEND : @R4V4N4
Python {}
Telethon {}

UserBot Forked from https://github.com/expectocode/uniborg""".format(
        sys.version,
        __version__
    )
    tgbotusername = Config.TG_BOT_USER_NAME_BF_HER
    if tgbotusername is not None:
        results = await borg.inline_query(tgbotusername, help_string)
        message = await results[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
        await event.delete()
    else:
        await event.edit(help_string)


@borg.on(events.NewMessage(pattern=r"\.dc", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetNearestDcRequest())
    await event.edit(result.stringify())


@borg.on(events.NewMessage(pattern=r"\.config", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    result = await borg(functions.help.GetConfigRequest())
    result = result.stringify()
    logger.info(result)
    await event.edit("""Telethon UserBot powered by @UniBorg""")
