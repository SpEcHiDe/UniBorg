""" Google Text to Speech
Available Commands:
.tr LanguageCode as reply to a message
.tr LangaugeCode | text to sepak"""

from googletrans import Translator
from telethon import events
from uniborg.util import admin_cmd


@borg.on(admin_cmd("tr ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "ml"
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.edit("`.tr LanguageCode` as reply to a message")
        return
    text = text.strip()
    lan = lan.strip()
    translator = Translator()
    try:
        translated = translator.translate(text, dest=lan)
        output_str = """**TRANSLATED** from {} to {}
{}""".format(
            translated.src,
            lan,
            translated.text
        )
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))
