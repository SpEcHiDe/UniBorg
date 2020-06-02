import asyncio
import html
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from uniborg.util import admin_cmd, is_admin
import sql_helpers.warns_sql as sql


@borg.on(admin_cmd(pattern="warn (.*)"))
async def _(event):
    if event.fwd_from:
        return
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    warn_reason = event.pattern_match.group(1)
    reply_message = await event.get_reply_message()
    
    if not admin and not creator:
        await event.edit("`Bruh I Am Not Admin Here`")
        return
    
    if await is_admin(event.chat_id, reply_message.from_id):
        return

    limit, soft_warn = sql.get_warn_setting(event.chat_id)
    num_warns, reasons = sql.warn_user(reply_message.from_id, event.chat_id, warn_reason)
    if num_warns >= limit:
        await event.client.edit_permissions(chat, reply_message.from_id, until_date=None, view_messages=False)
        if soft_warn:
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been kicked!".format(limit, reply_message.from_id)
            await event.client.kick_participant(event.chat_id, reply_message.from_id)
        else:
            await event.client.edit_permissions(chat, user.id, until_date=None, view_messages=False)
            reply = "{} warnings, <u><a href='tg://user?id={}'>user</a></u> has been banned!".format(limit, reply_message.from_id)
    else:
        reply = "<u><a href='tg://user?id={}'>user</a></u> has {}/{} warnings... watch out!".format(reply_message.from_id, num_warns, limit)
        if warn_reason:
            reply += "\nReason for last warn:\n{}".format(html.escape(warn_reason))
    #
    await event.edit(reply, parse_mode="html")


@borg.on(admin_cmd(pattern="get_warns"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    result = sql.get_warns(reply_message.from_id, event.chat_id)
    if result and result[0] != 0:
        num_warns, reasons = result
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if reasons:
            text = "This user has {}/{} warnings, for the following reasons:".format(num_warns, limit)
            text += "\r\n"
            text += reasons
            await event.edit(text)
        else:
            await event.edit("this user has {} / {} warning, but no reasons for any of them.".format(num_warns, limit))
    else:
        await event.edit("this user hasn't got any warnings!")


@borg.on(admin_cmd(pattern="reset_warns"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    sql.reset_warns(reply_message.from_id, event.chat_id)
    await event.edit("Warnings have been reset!")


@borg.on(admin_cmd(pattern="strongwarn ?(.*)"))
async def set_warn_strength(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    args = event.pattern_match.group(1)

    if not admin and not creator:
        await event.edit("`Bruh I Am Not Admin Here`")
        return

    if args:
        if args in ("on", "yes"):
            sql.set_warn_strength(event.chat_id, False)
            await event.edit("Warn Strength Set To Ban User.")
            return

        elif args in ("off", "no"):
            sql.set_warn_strength(event.chat_id, True)
            await event.edit("Warn Strength Set To Kick User.")
            return
       
        else:
            await event.edit("`Please send Correct Arg!`")
    else:
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        if soft_warn:
            await event.edit("I Am **kicking** User's For Now.")
        else:
            await event.edit("I Am **Baning** User's For Now.")
    return ""

@borg.on(admin_cmd(pattern="setwarnlimit ?(.*)"))
async def set_warn_limit(event):
    chat = await event.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    input_str = event.pattern_match.group(1)

    if not admin and not creator:
        await event.edit("`Bruh I Am Not Admin Here`")
        return
    
    if input_str:
        if int(input_str) < 3:
            await event.edit("`The minimum warn limit is 3!`")
        else:
            sql.set_warn_limit(event.chat_id, int(input_str))
            await event.edit("`Updated the warn limit to` {}".format(input_str))
            return
        
    else:
        limit, soft_warn = sql.get_warn_setting(event.chat_id)
        await event.edit("`The current warn limit is {}`".format(limit))
    return ""
