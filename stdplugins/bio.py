# For UniBorg
# By Priyam Kalra
# Syntax (.bio <text_to_set_as_bio>)
import asyncio
import time
from telethon.tl import functions
from telethon.errors import FloodWaitError
from uniborg.util import admin_cmd


DEL_TIME_OUT = 70


@borg.on(admin_cmd(pattern="bio ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    args = event.pattern_match.group(1)
    await event.delete()
    while True:
        DMY = time.strftime("%d.%m.%Y")
        HM = time.strftime("%H:%M:%S")
        bio1 = f"{DMY} "
        bio2 = f"| "
        bio3 = f" | "
        bio4 = f"{HM}"
        bio5 = bio1 + bio2 + args + bio3 + bio4
        logger.info(bio5)
        try:
            await borg(functions.account.UpdateProfileRequest(  # pylint:disable=E0602
                about=bio5
            ))
        except FloodWaitError as ex:
            logger.warning(str(e))
            await asyncio.sleep(ex.seconds)
        # else:
            # logger.info(r.stringify())
            # await borg.send_message(  # pylint:disable=E0602
            #     Config.PRIVATE_GROUP_BOT_API_ID,  # pylint:disable=E0602
            #     "Changed Profile Picture"
            # )
        await asyncio.sleep(DEL_TIME_OUT)
