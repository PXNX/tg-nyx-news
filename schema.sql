create table posts
(

    source_channel int,
    source_id      int,
    post_id        int,

    primary key (source_channel, source_id)
);