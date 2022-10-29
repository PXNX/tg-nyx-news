drop table posts;

create table posts
(

    source_channel bigint,
    source_id      int,
    post_id        int,
    reply_id int,

    primary key (source_channel, source_id)
);