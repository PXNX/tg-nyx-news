from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto, MessageMediaWebPage

from src.db import get_post


def get_reply(event):
    if event.original_update.message.reply_to is not None:

        reply = event.original_update.message.reply_to.reply_to_msg_id

        if reply is not None:
            return get_post(event.chat_id, reply)[0]


def get_media(event):
    m = event.original_update.message.media

    if m is None:
        return

    if type(m) is MessageMediaPhoto:
        return m.photo.id
    elif type(m) is MessageMediaDocument:
        return m.document.id
    elif type(m) is MessageMediaWebPage:
        if m.webpage.document is not None:
            return m.webpage.document.id
        else:
            return m.webpage.photo.id
    else:
        return None


def format_channel_id(channel_id: int) -> int:
    return int("-100" + str(channel_id))



