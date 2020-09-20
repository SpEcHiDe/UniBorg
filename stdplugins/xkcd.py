"""XKCD Search
Syntax: .xkcd <search>"""
from telethon.tl.types import Channel
import asyncio
import json
import requests
from urllib.parse import quote
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="xkcd ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    xkcd_id_s = []
    if input_str:
        if input_str.isdigit():
            xkcd_id_s = [input_str]
        else:
            xkcd_search_url = "https://relevantxkcd.appspot.com/process?"
            queryresult = requests.get(
                xkcd_search_url,
                params={
                    "action":"xkcd",
                    "query":quote(input_str)
                }
            ).text.strip()
            query_res = queryresult.split(" ")
            yreqsd = query_res[2:]
            xkcd_id_s = yreqsd[0::2]
    await event.edit(
        f"found {len(xkcd_id_s)} XKCD images, images will be sent soon"
    )
    cus = 0
    for xkcd_id in xkcd_id_s:
        xkcd_id = xkcd_id.strip()
        if xkcd_id is None:
            xkcd_url = "https://xkcd.com/info.0.json"
        else:
            xkcd_url = "https://xkcd.com/{}/info.0.json".format(xkcd_id)
        r = requests.get(xkcd_url)
        if r.ok:
            data = r.json()
            year = data.get("year")
            month = data["month"].zfill(2)
            day = data["day"].zfill(2)
            xkcd_link = "https://xkcd.com/{}".format(data.get("num"))
            safe_title = data.get("safe_title")
            transcript = data.get("transcript")
            alt = data.get("alt")
            img = data.get("img")
            title = data.get("title")
            link_preview = f"[\u2060]({img})"
            output_str = f"**{input_str}**\n"
            output_str += f"[XKCD ]({xkcd_link})\n"
            output_str += f"Title: {safe_title}\n"
            output_str += f"Alt: {alt}\n"
            output_str += f"Day: {day}\n"
            output_str += f"Month: {month}\n"
            output_str += f"Year: {year}\n"
            input_chat = await event.get_chat()
            if isinstance(input_chat, Channel) and input_chat.default_banned_rights.embed_links:
                rep = event
                if event.reply_to_msg_id:
                    rep = await event.get_reply_message()
                await rep.reply(output_str, link_preview=False, file=img)
                await event.delete()
            else:
                final_output = link_preview + output_str
                await event.reply(final_output, link_preview=True)
            cus += 1
        else:
            await event.edit("xkcd {} not found".format(xkcd_id))
    await event.edit(f"sent {cus} / {len(xkcd_id_s)} XKCD images")
