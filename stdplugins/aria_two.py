"""
A Torrent Client Plugin Based On Aria2 for Userbot

cmds: Magnet link : .magnet magnetLink
      Torrent file from local: .tor file_path
      Show Downloads: .show
      Remove All Downloads: .ariaRM
      Resume All Downloads: .ariaResume
      Pause All Downloads:  .ariaP

By:- @Zero_cool7870

Credits: https://github.com/jaskaranSM/UniBorg/blob/b42cd70144143ce079e5fb3aed49c9aa1412481b/stdplugins/aria.py
"""

import aria2p
import asyncio
import io
import os
from uniborg.util import admin_cmd

ARIA_2_PORT = 6800
cmd = f"aria2c --enable-rpc --rpc-listen-all=false --rpc-listen-port {ARIA_2_PORT}  --max-connection-per-server=10 --rpc-max-request-size=1024M --seed-time=0.01 --min-split-size=10M --follow-torrent=mem --split=10 --daemon=true"

aria2_is_running = os.system(cmd)

aria2 = aria2p.API(
    aria2p.Client(
        host="http://localhost",
        port=ARIA_2_PORT,
        secret=""
    )
)


@borg.on(admin_cmd("addmagnet"))
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.raw_text
    var = var.split(" ")
    magnet_uri = var[1]
    logger.info(magnet_uri)
    # Add Magnet URI Into Queue
    try:
        download = aria2.add_magnet(magnet_uri)
    except Exception as e:
        await event.edit("**Error**: __Make Sure Magnet link is correct.__\n`{}`".format(str(e)))
        return
    m = await event.reply("Downloading From Magnet Link:\nType `showariastatus` to check status")
    await asyncio.sleep(5)
    await m.delete()


@borg.on(admin_cmd("addtorrent"))
async def torrent_download(event):
    if event.fwd_from:
        return
    var = event.raw_text
    var = var.split(" ")
    torrent_file_path = var[1]
    logger.info(torrent_file_path)
    # Add Torrent Into Queue
    try:
        download = aria2.add_torrent(
            torrent_file_path, uris=None, options=None, position=None)
    except Exception as e:
        await event.edit("**Error**: __Make Sure Torrent PATH is correct.__\n`{}`".format(str(e)))
        return
    m = await event.reply("Downloading From given Link:\nType `showariastatus` to check status")
    await asyncio.sleep(5)
    await m.delete()


@borg.on(admin_cmd("ariaRM"))
async def remove_all(event):
    if event.fwd_from:
        return
    removed = aria2.remove_all()
    if removed == False:  # If API returns False Try to Remove Through System Call.
        os.system("aria2p remove-all")
    await event.edit("`Removed All Downloads.`")


@borg.on(admin_cmd("ariaP"))
async def pause_all(event):
    if event.fwd_from:
        return
    # Pause ALL Currently Running Downloads.
    paused = aria2.pause_all(force=True)
    await event.edit("Output: " + str(paused))


@borg.on(admin_cmd("ariaResume"))
async def resume_all(event):
    if event.fwd_from:
        return
    resumed = aria2.resume_all()
    await event.edit("Output: " + str(resumed))


@borg.on(admin_cmd("showariastatus"))
async def show_all(event):
    if event.fwd_from:
        return
    # Show All Downloads
    downloads = aria2.get_downloads()
    msg = ""
    for download in downloads:
        msg = msg + "File: " + str(download.name) + "\nSpeed: " + str(download.download_speed_string()) + "\n" + \
            "Progress: " + str(download.progress_string()) + \
            "\nETA:  " + str(download.eta_string()) + "\n\n"
    if len(msg) <= Config.MAX_MESSAGE_SIZE_LIMIT:
        await event.edit("`Current Downloads: `\n" + msg)
    else:
        with io.BytesIO(str.encode(msg)) as out_file:
            out_file.name = "ariastatus.txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="`Output is huge. Sending as a file...`"
            )
            await event.delete()
