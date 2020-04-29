# Copyleft 🄯 2017 UniBorg
#
# The below code might feel like copied, but
# https://t.me/MemeVideoBot?start=1333
#
# Licensed under the General Public License, Version 3 (the "License");
# you may use this file in compliance with the License.
#

"""RapidLeech plugin: Inspired by @SjProjects"""

import aiohttp
import asyncio
import json
import re
from bs4 import BeautifulSoup
from telethon.utils import get_inner_text
from uniborg.util import admin_cmd


logger.info(Config.OPEN_LOAD_LOGIN)
# https://t.me/RoseSupport/33801


@borg.on(admin_cmd(pattern="rl"))
async def _(event):
    if event.fwd_from:
        return
    current_message_text = event.raw_text
    cmt = current_message_text.split(" ")
    reply_message = await event.get_reply_message()
    if len(cmt) > 1:
        list_of_urls = cmt[1:]
    else:
        list_of_urls = get_inner_text(
            reply_message.message, reply_message.entities)
    converted_links = ""
    if len(list_of_urls) > 0:
        converted_links += "Trying to generate IP specific link\n\nഞെക്കി പിടി \n"
        for a_url in list_of_urls:
            converted_link_infos = await get_direct_ip_specific_link(a_url)
            if "url" in converted_link_infos:
                converted_link = converted_link_infos["url"]
                converted_links += f"[{a_url}]({converted_link}) \n\n"
            elif "err" in converted_link_infos:
                err = converted_link_infos["err"]
                converted_links += f"`{a_url}` returned `{err}`\n\n"
    await event.reply(converted_links)


async def get_direct_ip_specific_link(link: str):
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/openload.py#L246-L255
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/googledrive.py#L16-L27
    GOOGLE_DRIVE_VALID_URLS = r"(?x)https?://(?:(?:docs|drive)\.google\.com/(?:(?:uc|open)\?.*?id=|file/d/)|video\.google\.com/get_player\?.*?docid=)(?P<id>[a-zA-Z0-9_-]{28,})"
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/extractor/googledrive.py#L16-L27
    dl_url = None
    
    if re.search(GOOGLE_DRIVE_VALID_URLS, link):
        file_id = re.search(GOOGLE_DRIVE_VALID_URLS, link).group("id")
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar()) as session:
            step_zero_url = "https://drive.google.com/uc?export=download&id={}".format(file_id)
            http_response = await session.get(step_zero_url, allow_redirects=False)
            if "location" in http_response.headers:
                # in case of small file size, Google downloads directly
                file_url = http_response.headers["location"]
                if "accounts.google.com" in file_url:
                    dl_url = {
                        "err": "Private Google Drive URL"
                    }
                else:
                    dl_url = {
                        "url": file_url
                    }
            else:
                # in case of download warning page
                http_response_text = await http_response.text()
                response_b_soup = BeautifulSoup(http_response_text, "html.parser")
                warning_page_url = "https://drive.google.com" + response_b_soup.find("a", {"id": "uc-download-link"}).get("href")
                file_name_and_size = response_b_soup.find("span", {"class": "uc-name-size"}).text
                http_response_two = await session.get(warning_page_url, allow_redirects=False)
                if "location" in http_response_two.headers:
                    file_url = http_response_two.headers["location"]
                    if "accounts.google.com" in file_url:
                        dl_url = {
                            "err": "Private Google Drive URL"
                        }
                    else:
                        dl_url = {
                            "url": file_url,
                            "name": file_name_and_size
                        }
                else:
                    dl_url = {
                        "err": "Unsupported Google Drive URL"
                    }
    else:
        dl_url = {
            "err": "Unsupported URL. Try @transload"
        }
    return dl_url
