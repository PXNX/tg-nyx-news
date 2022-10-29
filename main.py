import re

from deep_translator import GoogleTranslator
from telethon import TelegramClient, events
from telethon.events import NewMessage, MessageEdited
from telethon.tl.types import UpdateNewChannelMessage, UpdateEditChannelMessage, MessageMediaWebPage

import config
from constant import TAG_TRAILING, HASHTAG, PLACEHOLDER, FLAG_EMOJI, TAG_EMPTY
from db import insert_post, Post, get_post, get_reply_id

client = TelegramClient("remove_inactive", config.api_id, config.api_hash)
client.parse_mode = 'html'


def get_reply(event):
    if event.original_update.message.reply_to is not None:

        reply = event.original_update.message.reply_to.reply_to_msg_id

        if reply is not None:
            return get_post(event.chat_id, reply)


def debloat(event):
    text = event.text

    if config.CHANNELS[event.chat_id].bloat is not None:
        bloats = [
            e.replace("/", r"\/").replace(".", r"\.").replace("+", r"\+").replace("|", r"\|")
            for e in config.CHANNELS[event.chat_id].bloat
        ]  # .replace("<strong>","").replace("</strong>","")
        print("bloats ::::", bloats, event.text)
        if len(bloats) != 0:
            for m in bloats:
                text = re.sub(m, '', text)
                print("replace::::::::::", text, "pattern ::::", m)

    print("debloat ::::", text)
    return text


def sanitize(text: str):
    cleaned_empty = re.sub(TAG_EMPTY, '', text)

    g = re.search(TAG_TRAILING, cleaned_empty)
    print("GROUP::::::::::::::::::::", cleaned_empty, g)

    if g is not None:
        for m in g.groups():
            cleaned_empty = re.sub(TAG_TRAILING, f"</{m}>", cleaned_empty, 1)
            print("MATCH ::::::::::::::", cleaned_empty)

    sub_text = re.sub(HASHTAG, '', cleaned_empty)
    print("subbbbbbbb ", sub_text)

    sub_text = sub_text.replace("<strong>", "<b>").replace("</strong>", "</b>").replace("<em>", "<i>").replace("</em>",
                                                                                                               "</i>")

    print("sanitized ::::", sub_text)
    return sub_text


def translate(event):
    if event.original_update.message.fwd_from is not None and event.original_update.message.fwd_from.from_id in list(
            config.CHANNELS.keys()):
        return

    sub_text = sanitize(debloat(event))

    emojis = re.findall(FLAG_EMOJI, sub_text)
    text_to_translate = re.sub(FLAG_EMOJI, PLACEHOLDER, sub_text)
    translated_text = GoogleTranslator(target="de").translate(text=text_to_translate)

    for emoji in emojis:
        translated_text = re.sub(PLACEHOLDER, emoji, translated_text, 1)

    print("translated_text :::::", translated_text)
    return f"{translated_text}\n\n<i>Quelle: <a href='tg://privatepost?channel={str(event.chat_id)[4:]}&post={event.original_update.message.id}'>{config.CHANNELS[event.chat_id].channel_name}{config.CHANNELS[event.chat_id].bias}</a></i>\n\n👉🏼 Folge @NYX_News für mehr!"


@client.on(events.Album(chats=list(config.CHANNELS.keys())))
async def handle_album(event):  # craft a new message and send
    print("album ------------------- ", event.stringify())
    text = translate(event)
    reply_id = get_reply(event)

    await client.send_message(config.POST_CHANNEL, file=event.messages, message=text, reply_to=reply_id)
    # ## or forward it directly # await event.forward_to(chat)


@client.on(events.NewMessage(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.NewMessage(chats=-1001391125365, outgoing=True))
async def post_text(event: NewMessage.Event):
    print(event.raw_text)
    print(event.stringify())

    text = translate(event)
    reply_id = get_reply(event)

    if type(event.original_update) is UpdateNewChannelMessage:
        print("send")

        if (
                event.photo is not None or event.video is not None) and type(
            event.media) is not MessageMediaWebPage:  # filter for media type???
            msg = await client.send_file(config.POST_CHANNEL, event.message.media, caption=text, reply_to=reply_id)
        else:
            msg = await client.send_message(config.POST_CHANNEL, text, link_preview=False, reply_to=reply_id)

        print(msg)

        insert_post(Post(event.chat_id, event.message.id, msg.id, reply_id))

    print("---end")


@client.on(events.MessageEdited(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.MessageEdited(chats=-1001391125365, outgoing=True))
async def edit_text(event: MessageEdited.Event):
    print("edit--------", event.raw_text)

    print(event.stringify())

    text = translate(event)

    if type(event.original_update) is UpdateEditChannelMessage:
        print("update")
        post_id = get_post(event.chat_id, event.message.id)
        print("post to update :::::::::::", post_id, type(post_id))

        if post_id is None:
            return await post_text(event)

        msg = await client.edit_message(config.POST_CHANNEL, post_id, text, link_preview=False)
        print(msg)

    # insert_post(Post(event.chat_id, event.message.id, msg.id))

    print("---end")


client.start()
print("-------------- start")
client.run_until_disconnected()
