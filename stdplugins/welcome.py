"""Greetings
Syntax: .savewelcome <Welcome Message>"""
from telethon import events

borg.storage.WELCOME = {}
borg.storage.last_welcome = {}


@borg.on(events.ChatAction())
async def welcome(event):
    if event.chat_id in borg.storage.WELCOME:
        # logger.info(event.stringify())
        """
        user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,
        """
        if event.user_joined:
            if event.chat_id in borg.storage.last_welcome:
                await borg.storage.last_welcome[event.chat_id].delete()
            try:
                user_ids = event.action_message.action.users
            except AttributeError as e:
                user_ids = [event.action_message.from_id]
            for user_id in user_ids:
                current_saved_welcome_message = borg.storage.WELCOME[event.chat_id]
                user_obj = await borg.get_entity(user_id)
                mention = "[{}](tg://user?id={})".format(user_obj.first_name, user_id)
                borg.storage.last_welcome[event.chat_id] = await event.reply(current_saved_welcome_message.format(mention=mention))
                try:
                    await event.delete()
                except Exception as e:
                    pass


@borg.on(events.MessageEdited(pattern=r"\.savewelcome (.*)", outgoing=True))
@borg.on(events.NewMessage(pattern=r"\.savewelcome (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    borg.storage.WELCOME[event.chat_id] = input_str
    await event.edit("Welcome note saved. ")
