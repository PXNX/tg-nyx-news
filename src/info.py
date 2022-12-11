from telethon import events
from telethon.events import NewMessage, Album

from config import CHANNEL_NEWS, CHANNEL_INFO
from main import client


@client.on(events.Album(chats=CHANNEL_INFO))
async def post_info_album(event: Album.Event):
    msg = await event.forward_to(CHANNEL_NEWS)
    await msg[0].pin()


@client.on(events.NewMessage(chats=CHANNEL_INFO, incoming=True, func=lambda a: a.grouped_id is None))
async def post_info(event: NewMessage.Event):
    msg = await event.forward_to(CHANNEL_NEWS)
    msg.pin()
