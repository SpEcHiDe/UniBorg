#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K
from math import ceil
import re
from telethon import events, custom


@borg.on(events.NewMessage(pattern=r"\.ib (.[^ ]*) (.*)", outgoing=True))
async def _(event):
    # https://stackoverflow.com/a/35524254/4723940
    if event.fwd_from:
        return
    bot_username = event.pattern_match.group(1)
    search_query = event.pattern_match.group(2)
    try:
        output_message = ""
        bot_results = await borg.inline_query(bot_username, search_query)
        i = 0
        for result in bot_results:
            output_message += "{} {} `{}`\n\n".format(
                result.title, result.description, ".icb " + bot_username + " " + str(i + 1) + " " + search_query)
            i = i + 1
        await event.edit(output_message)
    except Exception as e:
        await event.edit("{} did not respond correctly, for **{}**!\n `{}`".format(bot_username, search_query, str(e)))


@borg.on(events.NewMessage(pattern=r"\.icb (.[^ ]*) (.[^ ]*) (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.delete()
    bot_username = event.pattern_match.group(1)
    i_plus_oneth_result = event.pattern_match.group(2)
    search_query = event.pattern_match.group(3)
    try:
        bot_results = await borg.inline_query(bot_username, search_query)
        message = await bot_results[int(i_plus_oneth_result) - 1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
    except Exception as e:
        await event.edit(str(e))


if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.InlineQuery)
    async def inline_handler(event):
        builder = event.builder
        result = None
        if event.query.user_id == borg.uid:
            logger.info(event.stringify())
            query = event.text
            rev_text = query[::-1]
            if query.startswith("ping"):
                ping_place_rs = query.split(" ")[1]
                result = builder.article(
                    "© @UniBorg",
                    text="Pong\n{}".format(ping_place_rs),
                    buttons=[
                        [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url(
                            "Join the Group", "https://telegram.dog/ShrimadhaVahdamirhS")],
                        [custom.Button.url(
                            "Source Code", "https://GitLab.com/SpEcHiDe/UniBorg")]
                    ],
                    link_preview=False
                )
            elif "@UniBorg" in query:
                buttons = paginate_help(0, borg._plugins, "helpme")
                result = builder.article(
                    "© @UniBorg",
                    text="{}\nCurrently Loaded Plugins: {}".format(
                        query, len(borg._plugins)),
                    buttons=buttons,
                    link_preview=False
                )
            else:
                result = builder.article(
                    "© @UniBorg",
                    text=query,
                    buttons=[
                        [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url(
                            "Join the Group", "https://t.me/joinchat/AHAujEjG4FBO-TH-NrVVbg")],
                        [custom.Button.url(
                            "Source Code", "https://GitHub.com/SpEcHiDe/UniBorg")]
                    ],
                    link_preview=False
                )
        else:
            result = builder.article(
                "© @UniBorg",
                text="""Try @UniBorg
You can log-in as Bot or User and do many cool things with your Telegram account.

All instaructions to run @UniBorg in your PC has been explained in https://github.com/SpEcHiDe/UniBorg""",
                buttons=[
                    [custom.Button.url("Join the Channel", "https://telegram.dog/UniBorg"), custom.Button.url(
                        "Join the Group", "https://t.me/joinchat/AHAujEjG4FBO-TH-NrVVbg")],
                    [custom.Button.url(
                        "Source Code", "https://GitHub.com/SpEcHiDe/UniBorg")]
                ],
                link_preview=False
            )
        await event.answer([result] if result else None)


    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"helpme_next\((.+?)\)")))
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_help(current_page_number + 1, borg._plugins, "helpme")
        # logger.info(event.stringify())
        # https://t.me/TelethonChat/115200
        await event.edit(buttons=buttons)


    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"helpme_prev\((.+?)\)")))
    async def on_plug_in_callback_query_handler(event):
        current_page_number = int(event.data_match.group(1).decode("UTF-8"))
        buttons = paginate_help(current_page_number - 1, borg._plugins, "helpme")
        # logger.info(event.stringify())
        # https://t.me/TelethonChat/115200
        await event.edit(buttons=buttons)


    @tgbot.on(events.callbackquery.CallbackQuery(data=re.compile(b"ub_plugin_(.*)")))
    async def on_plug_in_callback_query_handler(event):
        plugin_name = event.data_match.group(1).decode("UTF-8")
        help_string = borg._plugins[plugin_name].__doc__[0:125]
        reply_pop_up_alert = help_string if help_string is not None else "No DOCSTRING has been setup for {} plugin".format(
            plugin_name)
        reply_pop_up_alert += "\n\n Use .unload {} to remove this plugin\n© @UniBorg".format(
            plugin_name)
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)


def paginate_help(page_number, loaded_plugins, prefix):
    helpable_plugins = []
    for p in loaded_plugins:
        if not p.startswith("_"):
            helpable_plugins.append(p)
    helpable_plugins = sorted(helpable_plugins)
    modules = [custom.Button.inline(
        "{} {}".format("✅", x),
        data="ub_plugin_{}".format(x))
        for x in helpable_plugins]
    pairs = list(zip(modules[::2], modules[1::2]))
    if len(modules) % 2 == 1:
        pairs.append((modules[-1],))
    max_num_pages = ceil(len(pairs) / 7)
    modulo_page = page_number % max_num_pages
    if len(pairs) > 7:
        pairs = pairs[modulo_page * 7:7 * (modulo_page + 1)] + \
                [
                    (custom.Button.inline("Previous", data="{}_prev({})".format(prefix, modulo_page)),
                    custom.Button.inline("Next", data="{}_next({})".format(prefix, modulo_page)))
                ]
    return pairs
