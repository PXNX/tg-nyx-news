import dataclasses
from typing import Optional, Tuple

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


def insert_source(source: Source):
    with conn.cursor() as c:
        res = c.execute(
            "insert into sources(channel_id,  detail_id, bias, description, rating, channel_name,display_name,invite,username) values (%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            (source.channel_id, source.detail_id, source.bias, source.description, source.rating, source.channel_name,
             source.display_name, source.invite, source.username))
        conn.commit()
        print(res)


def insert_post(post: Post):
    with conn.cursor() as c:
        res = c.execute(
            "insert into posts(channel_id, source_id, post_id, backup_id, reply_id, media_id) values (%s,%s,%s,%s,%s,%s);",
            (post.channel_id, post.source_id, post.post_id, post.backup_id, post.reply_id, post.media_id))
        conn.commit()
        print(res)


def get_post(channel_id: int, source_id: int) -> Tuple[int, int]:
    with conn.cursor() as c:
        c.execute("select post_id,backup_id from  posts where channel_id= %s and source_id = %s;",
                  (channel_id, source_id))
        res = c.fetchone()
        print(res)
        return res  # [0]


def get_reply_id(channel_id: int, source_id: int):
    with conn.cursor() as c:
        c.execute("select reply_id from  posts where channel_id = %s and source_id = %s;",
                  (channel_id, source_id))
        res = c.fetchone()
        print(res)
        if res is not None:
            return res[0]
        else:
            return res


def get_media_id(channel_id: int, source_id: int):
    with conn.cursor() as c:
        c.execute("select media_id from  posts where channel_id = %s and source_id = %s;",
                  (channel_id, source_id))
        res = c.fetchone()
        print(res)
        if res is not None:
            return res[0]
        else:
            return res


@dataclasses.dataclass
class SourceDAO:
    channel_id: int
    detail_id: int
    rating: int
    bias: str
    description: Optional[str]
    channel_name: str
    display_name: str
    invite: Optional[str]
    username: Optional[str]


def insert_source(source: SourceDAO):
    with conn.cursor() as c:
        c.execute(
            "insert into sources(channel_id, detail_id, rating, bias, description, channel_name, display_name, "
            "invite,username)  values(%s,%s,%s,%s,%s,%s,%s,%s,%s);",
            (source.channel_id, source.detail_id, source.rating, source.bias, source.description, source.channel_name,
             source.display_name, source.invite, source.username))
        conn.commit()
