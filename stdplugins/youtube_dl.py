#!/usr/bin/env python3
# This Source Code Form is subject to the terms of the GNU
# General Public License, v.3.0. If a copy of the GPL was not distributed with this
# file, You can obtain one at https://www.gnu.org/licenses/gpl-3.0.en.html
"""YoutubeDL
Click on any of the Buttons"""

import asyncio
import json
import os
import re
import time
from datetime import datetime
from telethon import custom, events


# pylint:disable=E0602
if Config.TG_BOT_USER_NAME_BF_HER is not None and tgbot is not None:
    @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
        data=re.compile(b"ytdl|(.*)|(.*)|(.*)")
    ))
    async def on_plug_in_callback_query_handler(event):
        if event.query.user_id == borg.uid:  # pylint:disable=E0602
            ctc, tg_send_type, ytdl_format_code, ytdl_extension = event.query.data.decode("UTF-8").split("|")
            try:
                with open(Config.TMP_DOWNLOAD_DIRECTORY + "/" + "YouTubeDL.json", "r", encoding="utf8") as f:
                    response_json = json.load(f)
            except FileNotFoundError as e:
                await event.edit("Something Bad Happened")
                return False
            custom_file_name = str(response_json.get("title")) + \
                "_" + ytdl_format_code + "." + ytdl_extension
            youtube_dl_url = response_json["webpage_url"]
            download_directory = Config.TMP_DOWNLOAD_DIRECTORY + "/" + custom_file_name
            command_to_exec = []
            if tg_send_type == "audio":
                command_to_exec = [
                    "youtube-dl",
                    "-c",
                    "--prefer-ffmpeg",
                    "--extract-audio",
                    "--audio-format", ytdl_extension,
                    "--audio-quality", ytdl_format_code,
                    youtube_dl_url,
                    "-o", download_directory
                ]
            else:
                minus_f_format = ytdl_format_code
                if "youtu" in youtube_dl_url:
                    minus_f_format = ytdl_format_code + "+bestaudio"
                command_to_exec = [
                    "youtube-dl",
                    "-c",
                    "--embed-subs",
                    "-f", minus_f_format,
                    "--hls-prefer-ffmpeg",
                    youtube_dl_url,
                    "-o", download_directory
                ]
            command_to_exec.append("--no-warnings")
            logger.info(command_to_exec)
            start = datetime.now()
            process = await asyncio.create_subprocess_exec(
                *command_to_exec,
                # stdout must a pipe to be accessible as process.stdout
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Wait for the subprocess to finish
            stdout, stderr = await process.communicate()
            e_response = stderr.decode().strip()
            t_response = stdout.decode().strip()
            # logger.info(e_response)
            # logger.info(t_response)
            ad_string_to_replace = "please report this issue on https://yt-dl.org/bug . Make sure you are using the latest version; see  https://yt-dl.org/update  on how to update. Be sure to call youtube-dl with the --verbose flag and include its complete output."
            if e_response and ad_string_to_replace in e_response:
                error_message = e_response.replace(ad_string_to_replace, "")
                await event.edit(error_message)
                return False
            if t_response:
                # logger.info(t_response)
                os.remove(Config.TMP_DOWNLOAD_DIRECTORY + "/" + "YouTubeDL.json")
                end_one = datetime.now()
                time_taken_for_download = (end_one -start).seconds
                await event.edit(f"Downloaded to `{download_directory}` in {time_taken_for_download} seconds")
            else:
                await event.delete()
        else:
            reply_pop_up_alert = "Please get your own @UniBorg, and don't waste my data! "
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
