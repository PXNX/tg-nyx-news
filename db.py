import dataclasses
from typing import Optional

import psycopg2
from psycopg2.extras import NamedTupleCursor

import config

# logger = logging.getLogger(__name__)
conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=NamedTupleCursor)


@dataclasses.dataclass
class Post:
    channel_id: int
    source_id: int
    post_id: int
    backup_id: int
    reply_id: Optional[int]
    media_id: Optional[str]


@dataclasses.dataclass
class Source:
    channel_id: int
    detail_id: int
    bias: Optional[str]
    description: str
    rating: int
    channel_name: str
    display_name: Optional[str]
    invite: Optional[str]
    username: Optional[str]

def insert_source(source:Source):
    with conn.cursor() as c:
        res = c.execute(
            "insert into sources(channel_id,  detail_id, bias, description, rating, channel_name,display_name,invite,username) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            (source.channel_id, source.detail_id,source.bias,source.description,source.rating,source.channel_name,source.display_name,source.invite,source.username))
        conn.commit()
        print(res)

def insert_post(post: Post):
    with conn.cursor() as c:
        res = c.execute(
            "insert into posts(channel_id, source_id, post_id, backup_id, reply_id, media_id) values (%s,%s,%s,%s,%s,%s);",
            (post.channel_id, post.source_id, post.post_id, post.backup_id, post.reply_id, post.media_id))
        conn.commit()
        print(res)


def get_post(source_channel: int, source_id: int):
    with conn.cursor() as c:
        c.execute("select post_id from  posts where source_channel = %s and source_id = %s;",
                  (source_channel, source_id))
        res = c.fetchone()
        print(res)
        if res is not None:
            return res[0]
        else:
            return res


def get_reply_id(source_channel: int, source_id: int):
    with conn.cursor() as c:
        c.execute("select reply_id from  posts where source_channel = %s and source_id = %s;",
                  (source_channel, source_id))
        res = c.fetchone()
        print(res)
        if res is not None:
            return res[0]
        else:
            return res


def get_media_id(source_channel: int, source_id: int):
    with conn.cursor() as c:
        c.execute("select media_id from  posts where source_channel = %s and source_id = %s;",
                  (source_channel, source_id))
        res = c.fetchone()
        print(res)
        if res is not None:
            return res[0]
        else:
            return res
