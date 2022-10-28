import dataclasses

import psycopg2
from psycopg2.extras import NamedTupleCursor

import config

# logger = logging.getLogger(__name__)
conn = psycopg2.connect(config.DATABASE_URL, cursor_factory=NamedTupleCursor)


@dataclasses.dataclass
class Post:
    source_channel: int
    source_id: int
    post_id: int


def insert_post(post: Post):
    with conn.cursor() as c:
        res = c.execute("insert into posts(source_channel, source_id, post_id) values (%s,%s,%s);",
                        (post.source_channel, post.source_id, post.post_id))
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
