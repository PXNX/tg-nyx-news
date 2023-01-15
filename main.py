import logging
import logging
import re

from telethon import TelegramClient, events
from telethon.events import NewMessage, MessageEdited, Album
from telethon.tl.types import UpdateNewChannelMessage, UpdateEditChannelMessage, MessageMediaWebPage, MessageMediaPoll, \
    MessageMediaDocument

from config import CHANNEL_NEWS, api_id, api_hash, CHANNEL_BACKUP, CHANNEL_MEME
from src.db import get_post, insert_post, Post
from src.input import source_ids, get_active_sources, get_all_sources
from src.log import init_logger
from src.translate import translate, format_text, translate_text
from src.util import get_reply, get_media, format_channel_id

init_logger()

client = TelegramClient('sessionfile2', api_id, api_hash)


def getcode() -> str:
    code = input("Code :::")
    return code


client.start(phone="491773000756", password="area", code_callback=getcode)
client.parse_mode = 'html'


@client.on(events.Album(chats=CHANNEL_NEWS))
async def handle_album_own(event: Album.Event):
    if event.original_update.message.fwd_from is not None:
        channel_id = format_channel_id(event.original_update.message.fwd_from.from_id.channel_id)
        if channel_id == CHANNEL_MEME:
            return
        print(event.stringify() + " ----------- HAO ---")
        try:
            await post_album(event, channel_id)
        except Exception as e:
            logging.exception(e)
            pass
        await client.delete_messages(event.chat_id, [x.id for x in event.messages])


@client.on(events.Album(chats=source_ids))
async def handle_album(event: Album.Event):  # craft a new message and send

    print("album ------------------- ", event.stringify())
    logging.debug("--------- post ALBUM :::", event.stringify())

    if event.original_update.message.fwd_from is not None:  ##### and event.original_update.message.fwd_from.from_id in source_ids:
        return

    await post_album(event)


async def post_album(event: Album.Event, chat_id=None):
    if chat_id is None:
        chat_id = event.chat_id

    translated_text = await translate(event, chat_id)
    if translated_text is None:
        return

    backup_id = (await event.forward_to(CHANNEL_BACKUP))[
        0].id  # todo: make it handle whole album here and also save media_id of every entry

    text = format_text(translated_text, event, backup_id, chat_id)

    reply_id = get_reply(event)

    for m in event.messages:
        logging.info(f"media ::::::::::::::::::::::::::::::: ALBUM ::: ")  # {m.media.photo.id}

    try:
        msg = await client.send_message(CHANNEL_NEWS, file=event.messages, message=text, reply_to=reply_id)
        print(f"SENT ALBUM ________________________ :::: {msg}")
        insert_post(Post(chat_id, event.original_update.message.id, msg.id, backup_id, reply_id, None))
    except Exception as e:
        print(f"‼️ Error when sending Album: {e}")

    print("--- end ALBUM")


@client.on(events.NewMessage(chats=CHANNEL_NEWS, incoming=True, func=lambda a: a.grouped_id is None))
# @client.on(events.NewMessage(chats=CHANNEL_NEWS, outgoing=True, func=lambda a: a.grouped_id is None))
async def post_text_own(event: NewMessage.Event):
    print(event.stringify() + " ---------------------------- pto")
    if event.original_update.message.fwd_from is not None:
        channel_id = format_channel_id(event.original_update.message.fwd_from.from_id.channel_id)
        if channel_id == CHANNEL_MEME:
            return

        print(event.stringify() + "------------------------------------------------ PTO if")
        try:

            await post_text(event, channel_id)
        except Exception as e:
            logging.exception(e)
            pass
        print("-- post text own END --")
        await client.delete_messages(event.chat_id, event.message.id)


# todo: maybe add a functionality where you can send something to the bot account and it will then post in channel?
@client.on(events.NewMessage(chats=source_ids, incoming=True, func=lambda a: a.grouped_id is None))
# @client.on(events.NewMessage(chats=-1001391125365, outgoing=True, func= lambda a: a.grouped_id is None))
async def handle_text(event: NewMessage.Event):
    #   print(event.raw_text)
    print("--------- post TEXT:::", event.stringify())
    logging.debug("--------- post TEXT:::", event.stringify())

    if event.original_update.message.fwd_from is not None:  ##### and event.original_update.message.fwd_from.from_id in source_ids:
        return

    # if get_media(event) is not None and get_media_id(event.chat_id, event.original_update.message.id) == get_media(
    #      event):
    #   print("---------\n\n\n A L R E A D Y  -- P R E S E N T\n\n\n---------")
    #   return
    await post_text(event)


async def post_text(event: NewMessage.Event, chat_id=None):
    print("Handle Text")

    if type(event.original_update) is UpdateNewChannelMessage and event.original_update.message.grouped_id is None and type(
            event.media) is not MessageMediaPoll and type(event) is NewMessage.Event:
        print("send")

        if chat_id is None:
            chat_id = event.chat_id

        translated_text = await translate(event, chat_id)
        print(translated_text)
        if translated_text is None:
            return

        backup_id = (await event.forward_to(CHANNEL_BACKUP)).id

        text = format_text(translated_text, event, backup_id, chat_id)

        reply_id = get_reply(event)

        print("sendd")

        try:
            if event.message.media is not None and len(text) <= 1000:  # filter for media type???
                print("has media")

                if type(event.message.media) is MessageMediaDocument and event.message.media.document.mime_type.startswith(
                        "audio"):
                    return

                print(f"media ::::::::::::::::::::::::::::::: {get_media(event)}")

                if type(event.message.media) is MessageMediaWebPage:

                    await client.send_message(703453307,
                                              f"MessageMediaWebPage ‼\n\nTitle: <code>{event.message.media.webpage.title}</code>\n\n\nId: <code>{event.message.id}</code>\n\n\nMedia: <code>{event.message.media}</code>")

                    if event.message.media.webpage.title is not None and len(
                            re.findall(r"t\.me/", event.message.media.webpage.url)) == 0:
                        formatted_text = f"<b>{translate_text(event.message.media.webpage.title)}</b>\n\n{text}"
                    else:
                        formatted_text = text

                    if event.message.media.webpage.photo is not None and event.message.media.webpage.type != 'video':
                        media = event.message.media.webpage.photo
                    elif event.message.media.webpage.photo is not None and event.message.media.webpage.type == 'video':
                        # todo: find a way to download videos
                        media = event.message.media.webpage.photo
                    else:  # todo: just send text then?
                        msg = await client.send_message(CHANNEL_NEWS, formatted_text, link_preview=False,
                                                        reply_to=reply_id)
                        insert_post(Post(chat_id, event.message.id, msg.id, backup_id, reply_id, None))
                        return

                    msg = await client.send_file(CHANNEL_NEWS, media, caption=formatted_text, reply_to=reply_id)

                else:
                    msg = await client.send_file(CHANNEL_NEWS, event.message.media, caption=text, reply_to=reply_id)

                    insert_post(Post(chat_id, event.message.id, msg.id, backup_id, reply_id, get_media(event)))

            else:

                msg = await client.send_message(CHANNEL_NEWS, text, link_preview=False, reply_to=reply_id)
                insert_post(Post(chat_id, event.message.id, msg.id, backup_id, reply_id, None))

            print(msg)


        except Exception as e:
            print(f"‼️ Error when sending Message: {e}")
            logging.exception("‼️ Error when sending Message", e)

    print("---end SEND")


@client.on(events.MessageEdited(chats=source_ids, incoming=True))
# @client.on(events.MessageEdited(chats=list(OWN_SOURCES.keys()), outgoing=True))
async def edit_text(event: MessageEdited.Event):
    print("edit--------", event.raw_text)

    print(event.stringify())

    if type(event.original_update) is UpdateEditChannelMessage:
        print("--- update ---")
        #   print("update")
        (post_id, backup_id) = get_post(event.chat_id, event.message.id)
        #  print("post to update :::::::::::", post_id, type(post_id))
        print("--- edit ::: post_id :::::", post_id)

        if post_id is None:
            await handle_text(event)

        try:
            text = format_text(await translate(event), event, backup_id)

            msg = await client.edit_message(CHANNEL_NEWS, post_id, text,
                                            link_preview=False)  # todo: does that even work?
            print(msg)
        except Exception as e:
            if e.__class__.__name__ != "MessageNotModifiedError":
                print(f"‼️ Error when editing Message: {e}")
                logging.exception("‼️ Error when editing Message", e)

    # insert_post(Post(event.chat_id, event.message.id, msg.id))

    print("---end EDIT")


get_active_sources()
get_all_sources()
print("### STARTED ###")
logging.info("### STARTED ###")
client.run_until_disconnected()
