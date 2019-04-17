from io import BytesIO

from uniborg import util

from telethon import types
from telethon.errors import PhotoInvalidDimensionsError
from telethon.tl.functions.messages import SendMediaRequest


@borg.on(util.admin_cmd(r"f"))
async def on_file_to_photo(event):
    await event.delete()
    target = await event.get_reply_message()
    try:
        image = target.media.document
    except AttributeError:
        return
    if not image.mime_type.startswith('image/'):
        return  # This isn't an image
    if image.mime_type == 'image/webp':
        return  # Telegram doesn't let you directly send stickers as photos
    if image.size > 10 * 1024 * 1024:
        return  # We'd get PhotoSaveFileInvalidError otherwise

    file = await borg.download_media(target, file=BytesIO())
    file.seek(0)
    img = await borg.upload_file(file)
    img.name = 'image.png'

    try:
        await borg(SendMediaRequest(
            peer=await event.get_input_chat(),
            media=types.InputMediaUploadedPhoto(img),
            message=target.message,
            entities=target.entities,
            reply_to_msg_id=target.id
        ))
    except PhotoInvalidDimensionsError:
        return