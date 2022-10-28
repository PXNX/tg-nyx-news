import re

from deep_translator import GoogleTranslator
from telethon import TelegramClient, events
from telethon.events import NewMessage, MessageEdited
from telethon.tl.types import UpdateNewChannelMessage, UpdateEditChannelMessage

import config
from db import insert_post, Post, get_post

client = TelegramClient("remove_inactive", config.api_id, config.api_hash)
client.parse_mode = 'html'


def translate(event):
    if event.message.fwd_from is not None and event.message.fwd_from.from_id in list(config.CHANNELS.keys()):
        return

    footer = config.CHANNELS[event.chat_id].footer.replace("/", r"\/").replace(".", r"\.").replace("+", r"\+").replace(
        "'", "\"").replace("|", r"\|")
    print(footer)
    if footer != "":
        matches = re.findall(footer, event.text)
        print(matches, event.text)
        if len(matches) == 0:
            return  # because some have their ads without footer

    sub_text = re.sub(r"\s*((#\w+)*\s*)*\s*" + footer + r"\s*$", '', event.text)
    emojis = re.findall(config.FLAG_EMOJI, sub_text)
    text_to_translate = re.sub(config.FLAG_EMOJI, config.PLACEHOLDER, sub_text)
    translated_text = GoogleTranslator(target="de").translate(text=text_to_translate)
    for emoji in emojis:
        translated_text = re.sub(config.PLACEHOLDER, emoji, translated_text, 1)

    print("translated_text :::::", translated_text)
    return f"{translated_text}\n\n<i>Quelle: <a href='tg://privatepost?channel={str(event.chat_id)[4:]}&post={event.message.id}'>{config.CHANNELS[event.chat_id].channel_name}{config.CHANNELS[event.chat_id].bias}</a></i>\n\n👉🏼 Folge @NYX_News für mehr!"


@client.on(events.Album(chats=list(config.CHANNELS.keys())))
async def handle_album(event):  # craft a new message and send
    print("album ------------------- ", event.stringify())
    text = translate(event)

    await client.send_message(config.POST_CHANNEL, file=event.messages, message=text, )
    # ## or forward it directly # await event.forward_to(chat)


@client.on(events.NewMessage(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.NewMessage(chats=-1001391125365, outgoing=True))
async def post_text(event: NewMessage.Event):
    print(event.raw_text)

    print(event.stringify())

    text = translate(event)

    if type(event.original_update) is UpdateNewChannelMessage:
        print("send")

        if event.message.media is not None:
            msg = await client.send_file(config.POST_CHANNEL, event.message.media, caption=text)
        else:
            msg = await client.send_message(config.POST_CHANNEL,
                                            text, link_preview=False)

        print(msg)

        insert_post(Post(event.chat_id, event.message.id, msg.id))

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
        msg = await client.edit_message(config.POST_CHANNEL, post_id,
                                        text)
        print(msg)

    # insert_post(Post(event.chat_id, event.message.id, msg.id))

    print("---end")


client.start()
print("-------------- start")
client.run_until_disconnected()
