"""Greetings
Commands:
.clearwelcome
.savewelcome <Welcome Message>"""

from telethon import events
from sql_helpers.welcome_sql import get_current_welcome_settings, \
    add_welcome_setting, rm_welcome_setting, update_previous_welcome
from uniborg.util import admin_cmd


@borg.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
    cws = get_current_welcome_settings(event.chat_id)
    if cws:
        # logger.info(event.stringify())
        """user_added=False,
        user_joined=True,
        user_left=False,
        user_kicked=False,"""
        if event.user_joined:
            if cws.should_clean_welcome:
                try:
                    await borg.delete_messages(  # pylint:disable=E0602
                        event.chat_id,
                        cws.previous_welcome
                    )
                except Exception as e:  # pylint:disable=C0103,W0703
                    logger.warn(str(e))  # pylint:disable=E0602
            try:
                user_ids = event.action_message.action.users
            except AttributeError:
                user_ids = [event.action_message.from_id]
            for user_id in user_ids:
                current_saved_welcome_message = cws.custom_welcome_message
                user_obj = await borg.get_entity(user_id)  # pylint:disable=E0602
                mention = "[{}](tg://user?id={})".format(user_obj.first_name, user_id)
                current_message = await event.reply(
                    current_saved_welcome_message.format(mention=mention)
                )
                update_previous_welcome(event.chat_id, current_message.id)


@borg.on(admin_cmd("savewelcome (.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    add_welcome_setting(event.chat_id, input_str, True, 0)
    await event.edit("Welcome note saved. ")


@borg.on(admin_cmd("clearwelcome"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    cws = get_current_welcome_settings(event.chat_id)
    rm_welcome_setting(event.chat_id)
    await event.edit(
        "Welcome note cleared. " + \
        "The previous welcome message was `{}`.".format(cws.custom_welcome_message)
    )
