"""Default Permission in Telegram 5.0.1
Syntax: .lock <option>
Available Options: msg, media, sticker, gif, gamee, ainline, gpoll, adduser, cpin, changeinfo"""
from telethon import events, functions, types
import asyncio


@borg.on(events.NewMessage(pattern=r"\.lock ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if "msg" in input_str:
        msg = True
    if "media" in input_str:
        media = True
    if "sticker" in input_str:
        sticker = True
    if "gif" in input_str:
        gif = True
    if "gamee" in input_str:
        gamee = True
    if "ainline" in input_str:
        ainline = True
    if "gpoll" in input_str:
        gpoll = True
    if "adduser" in input_str:
        adduser = True
    if "cpin" in input_str:
        cpin = True
    if "changeinfo" in input_str:
        changeinfo = True
    banned_rights=types.ChatBannedRights(
        until_date=None,
        # view_messages=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        result = await borg(functions.messages.EditChatDefaultBannedRightsRequest(
            peer=peer_id,
            banned_rights=banned_rights
        ))
        # logger.info(result.stringify())
    except Exception as e:
        await event.edit(str(e))
    else:
        await event.edit("Current Chat Default Permissions Changed Successfully")
