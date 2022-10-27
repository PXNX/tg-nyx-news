import asyncio
import dataclasses
import logging

from deep_translator import GoogleTranslator
from telethon import TelegramClient, events
from telethon.events import NewMessage
from telethon.tl.types import UpdateNewChannelMessage

import config

client = TelegramClient("remove_inactive", config.api_id, config.api_hash)
client.parse_mode = 'html'


@client.on(events.NewMessage(chats=list(config.CHANNELS.keys()), incoming=True))
@client.on(events.NewMessage(chats=-1001391125365, outgoing=True))
async def my_event_handler(event: NewMessage.Event):
    print(event.raw_text)

    print(event.stringify())

    translated_text = GoogleTranslator(target="de").translate(text=event.raw_text)
    print(translated_text)

    if type(event.original_update) is UpdateNewChannelMessage:
        print("send")
        await client.send_message(config.POST_CHANNEL,
                                  translated_text + f"\n\n<a href='tg://privatepost?channel={str(event.chat_id)[4:]}&post={event.message.id}'>➡️ {config.CHANNELS[event.chat_id]}</a>")
    print("---end")


client.start()
print("-------------- start")
client.run_until_disconnected()


@dataclasses.dataclass
class Post:
    source_channel: int
    source_id: int
    post_id: int


logger = logging.getLogger(__name__)
conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=NamedTupleCursor)


def insert_post(post: Post):
    with conn.cursor() as c:
        c.execute("insert into posts(source_channel, source_id, post_id) values (%s,%s,%s)",
            (post.source_channel, post.source_id, post.post_id))
        conn.commit()
