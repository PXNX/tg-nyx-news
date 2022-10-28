from deep_translator import GoogleTranslator
from telethon import TelegramClient, events
from telethon.events import NewMessage
from telethon.tl.types import UpdateNewChannelMessage, UpdateEditChannelMessage

import config
from db import insert_post, Post, get_post

client = TelegramClient("remove_inactive", config.api_id, config.api_hash)
client.parse_mode = 'html'


@client.on(events.NewMessage(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.NewMessage(chats=-1001391125365, outgoing=True))
async def post_text(event: NewMessage.Event):
    print(event.raw_text)

    print(event.stringify())

    translated_text = GoogleTranslator(target="de").translate(text=event.raw_text)
    formatted_text = translated_text + f"\n\n<a href='tg://privatepost?channel={str(event.chat_id)[4:]}&post={event.message.id}'>➡️ {config.CHANNELS[event.chat_id]}</a>"
    print(translated_text)

    if type(event.original_update) is UpdateNewChannelMessage:
        print("send")

        if event.message.media is not None:

            msg = await client.send_file(config.POST_CHANNEL, event.message.media, caption= formatted_text )
        else:
            msg = await client.send_message(config.POST_CHANNEL,
                                            formatted_text)

        print(msg)

        insert_post(Post(event.chat_id, event.message.id, msg.id))

    print("---end")


@client.on(events.MessageEdited(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.MessageEdited(chats=-1001391125365, outgoing=True))
async def edit_text(event: NewMessage.Event):
    print("edit--------", event.raw_text)

    print(event.stringify())

    translated_text = GoogleTranslator(target="de").translate(text=event.raw_text)
    print(translated_text)

    if type(event.original_update) is UpdateEditChannelMessage:
        print("update")
        post_id = get_post(event.chat_id, event.message.id)
        msg = await client.edit_message(config.POST_CHANNEL, post_id,
                                        translated_text + f"\n\n<a href='tg://privatepost?channel={str(event.chat_id)[4:]}&post={event.message.id}'>➡️ {config.CHANNELS[event.chat_id]}</a>")
        print(msg)

    # insert_post(Post(event.chat_id, event.message.id, msg.id))

    print("---end")


client.start()
print("-------------- start")
client.run_until_disconnected()
