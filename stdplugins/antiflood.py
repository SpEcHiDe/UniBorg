from telethon import events
import asyncio
from telethon.tl.functions.channels import EditBannedRequest


borg.storage.CHAT_FLOOD = {}


@borg.on(events.NewMessage(chats=Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD))
async def _(event):
    chat = await event.get_chat()
    if not event.chat_id in borg.storage.CHAT_FLOOD:
        borg.storage.CHAT_FLOOD[event.chat_id] = {}
    if event.chat_id in borg.storage.CHAT_FLOOD:
        try:
            max_count = int(borg.storage.CHAT_FLOOD[event.chat_id][2]) or Config.MAX_ANTI_FLOOD_MESSAGES
        except KeyError as e:
            max_count = Config.MAX_ANTI_FLOOD_MESSAGES
        if event.message.from_id in borg.storage.CHAT_FLOOD[event.chat_id]:
            current_count = int(borg.storage.CHAT_FLOOD[event.chat_id][1])
            current_count += 1
            if current_count > max_count:
                try:
                    await borg(EditBannedRequest(event.chat_id, event.message.from_id, Config.ANTI_FLOOD_WARN_MODE))
                except (Exception) as exc:
                    m1 = await borg.send_message(
                        entity=event.chat_id,
                        message="**Automatic AntiFlooder**\n @admin [User](tg://user?id={}) is flooding this chat. \n`{}`".format(event.message.from_id, str(exc)),
                        reply_to=event.message.id
                    )
                    await asyncio.sleep(10)
                    await m1.edit("https://t.me/keralagram/724970")
                else:
                    await borg.send_message(
                        entity=event.chat_id,
                        message="**Automatic AntiFlooder**\n[User](tg://user?id={}) has been automatically restricted because he reached the defined flood limit.".format(event.message.from_id),
                        reply_to=event.message.id
                    )
                borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, 0, max_count)
            else:
                borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, current_count, max_count)
        else:
            borg.storage.CHAT_FLOOD[event.chat_id] = (event.message.from_id, 1, max_count)


@borg.on(events.NewMessage(pattern=r"\.setflood (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if event.chat_id not in Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD:
        Config.CHATS_TO_MONITOR_FOR_ANTI_FLOOD.append(event.chat_id)
    input_str = event.pattern_match.group(1)
    try:
        borg.storage.CHAT_FLOOD[event.chat_id] = (None, 1, int(input_str))
        await event.edit("Antiflood updated to {} in the current chat".format(input_str))
    except Exception as e:
        await event.edit(str(e))
