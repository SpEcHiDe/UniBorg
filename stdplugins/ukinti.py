""" @ukinti_bot
Available Commands:
.unbanall
.kick option
Available Options: d, y, m, w, o, q, r """
from telethon import events
from datetime import datetime, timedelta
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from telethon.tl import functions, types
from time import sleep
import asyncio
from uniborg.util import admin_cmd


@borg.on(admin_cmd("unbanall ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        await event.edit("Searching Participant Lists.")
        p = 0
        async for i in borg.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(
                until_date=0,
                view_messages=False
            )
            try:
                await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
            except UserNotParticipantError as ex:
                pass
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await event.edit(str(ex))
            else:
                p += 1
        await event.edit("{}: {} unbanned".format(event.chat_id, p))


@borg.on(admin_cmd("kick ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    p = 0
    c = 0
    d = 0
    e = []
    m = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    await event.edit("Searching Participant Lists.")
    async for i in borg.iter_participants(event.chat_id, aggressive=True):
        p = p + 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        if i.deleted:
            d = d + 1
            if input_str == "d":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusEmpty:
            y = y + 1
            if input_str == "y":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusLastMonth:
            m = m + 1
            if input_str == "m":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusLastWeek:
            w = w + 1
            if input_str == "w":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusOffline:
            o = o + 1
            if input_str == "o":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusOnline:
            q = q + 1
            if input_str == "q":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
        if type(i.status) is UserStatusRecently:
            r = r + 1
            if input_str == "r":
                try:
                    await borg(functions.channels.EditBannedRequest(event.chat_id, i, rights))
                    c = c + 1
                except UserAdminInvalidError as exc:
                    await event.edit("I need admin priveleges to perform this action!")
                    break
                except:
                    e.append("ERROR")
    required_string = """Kicked {} / {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}
    """
    await event.edit(required_string.format(c, p, d, y, m, w, o, q, r))
    await asyncio.sleep(5)
    await event.edit("""Total: {} users
Deleted Accounts: {}
UserStatusEmpty: {}
UserStatusLastMonth: {}
UserStatusLastWeek: {}
UserStatusOffline: {}
UserStatusOnline: {}
UserStatusRecently: {}""".format(p, d, y, m, w, o, q, r))
