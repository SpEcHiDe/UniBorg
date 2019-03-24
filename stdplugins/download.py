"""Download Files to your local server
Syntax:
.download as reply to a Telegram media
.download url | file.name to download files from a Public Link"""
from telethon import events
import aiohttp
import asyncio
import json
import os
import requests
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

import time
from uniborg.util import progress, humanbytes, TimeFormatter


@borg.on(events.NewMessage(pattern=r"\.download ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Processing 🙇🏼‍♂️...")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        c_time = time.time()
        downloaded_file_name = await borg.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, event, c_time, "trying to download 🧐")
            )
        )
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Downloaded to `{}` in {} seconds😃✅.".format(downloaded_file_name, ms))
    elif input_str:
        start = datetime.now()
        url = input_str
        file_name = os.path.basename(url)
        to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
        if "|" in input_str:
            url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        async with aiohttp.ClientSession() as session:
            c_time = time.time()
            await download_coroutine(
                session,
                url,
                downloaded_file_name,
                event,
                c_time
            )
        end = datetime.now()
        ms = (end - start).seconds
        if os.path.exists(downloaded_file_name):
            await event.edit("Downloaded to `{}` in {} seconds😃✅.".format(downloaded_file_name, ms))
        else:
            await event.edit("⛔️😬Incorrect URL\n {}".format(input_str))
    else:
        await event.edit("‼️Reply to a message to download to my local server😅.")


async def download_coroutine(session, url, file_name, event, start):
    CHUNK_SIZE = 2341
    downloaded = 0
    display_message = ""
    async with session.get(url) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await event.edit("""🙇🏻‍♂️Initiating Download
URL: {}
File Name: {}
File Size: {}""".format(url, file_name, humanbytes(total_length)))
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """🛑**Download Status**🛑
URL: {}
File Name: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(url, file_name, humanbytes(total_length), humanbytes(downloaded), TimeFormatter(estimated_total_time))
                        if current_message != display_message:
                            await event.edit(current_message)
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
