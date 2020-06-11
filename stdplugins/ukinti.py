""" @ukinti_bot
Available Commands:
.unbanall
.kick option
Available Options: d, y, m, w, o, q, r """
from telethon import events
from datetime import datetime, timedelta
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, \
    UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from telethon.tl import functions, types
from time import sleep
import asyncio
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="unbanall ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if input_str:
        logger.info("TODO: Not yet Implemented")
    else:
        if event.is_private:
            await event.edit("Only works in Groups/Channels")
            return False
        await event.edit("Searching Participant Lists.")
        participants_count = 0
        async for kicked_user in borg.iter_participants(event.chat_id, filter=ChannelParticipantsKicked, aggressive=True):
            rights = ChatBannedRights(
                until_date=0,
                view_messages=False
            )
            try:
                await borg(functions.channels.EditBannedRequest(channel = event.chat_id, user_id = kicked_user, banned_rights = rights))
            except FloodWaitError as ex:
                logger.warn("sleeping for {} seconds".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await event.edit(str(ex))
            else:
                participants_count += 1
        await event.edit("{}: {} participants unbanned".format(event.chat_id, participants_count))


@borg.on(admin_cmd(pattern="kick ?(.*)"))  # Is it ikuck or kick?
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        await event.edit("Only works in Groups/Channels")
        return False
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not (chat.admin_rights or chat.creator):
            await event.edit("`You aren't an admin here!`")
            return False
    participants_count = 0
    bots = 0
    c = 0
    deleted_accts = 0
    ee = []
    m = 0
    user_status_none = 0
    y = 0
    w = 0
    o = 0
    users_online = 0
    active_users = 0
    await event.edit("Searching Participant Lists.")
    #
    # Note that it's "reversed". You must set to ``True`` the permissions
    # you want to REMOVE, and leave as ``None`` those you want to KEEP.
    rights = ChatBannedRights(
        until_date=None,
        view_messages=True
    )
    async for user in borg.iter_participants(event.chat_id):
        participants_count = participants_count + 1
        
        if isinstance(user.status, UserStatusEmpty):
            y = y + 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin privileges to perform this action!")
                        # TODO check admin privileges before iteratin'
                    except:
                        pass
                    ee.append(str(e))
                    break  # FIXME If privileges checked before iteration, we could remove this break
                else:
                    c = c + 1
        elif isinstance(user.status, UserStatusLastMonth):
            m = m + 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif isinstance(user.status, UserStatusLastWeek):
            w = w + 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif isinstance(user.status, UserStatusOffline):
            o = o + 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif isinstance(user.status, UserStatusOnline):
            users_online = users_online + 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif isinstance(user.status, UserStatusRecently):
            active_users = active_users + 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        if user.bot:
            bots = bots + 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif user.deleted:
            deleted_accts = deleted_accts + 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, user, rights)
                if not status:
                    try:
                        await event.edit("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
                    break
                else:
                    c = c + 1
        elif user.status is None:
            user_status_none = user_status_none + 1
    if input_str:
        required_string = """
        Kicked {} / {} users
        Deleted Accounts: {}
        UserStatusEmpty: {}
        UserStatusLastMonth: {}
        UserStatusLastWeek: {}
        UserStatusOffline: {}
        UserStatusOnline: {}
        UserStatusRecently: {}
        Bots: {}
        None: {}"""
        await event.edit(required_string.format(c, participants_count, deleted_accts, y, m, w, o, users_online, active_users, bots, user_status_none))
        await asyncio.sleep(5)
    else:
        await event.edit("""
        Total: {} users
        Deleted Accounts: {}
        UserStatusEmpty: {}
        UserStatusLastMonth: {}
        UserStatusLastWeek: {}
        UserStatusOffline: {}
        UserStatusOnline: {}
        UserStatusRecently: {}
        Bots: {}
        None: {}""".format(participants_count, deleted_accts, y, m, w, o, users_online, active_users, bots, user_status_none))


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)
