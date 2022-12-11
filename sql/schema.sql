drop table posts;
--ALTER TABLE posts ADD COLUMN  media_id bigint;

create table sources
(

    channel_id bigint not null,
    detail_id      int not null,
   rating       int not null,
    bias text,
    description text,
    channel_name varchar(128) not null,
    display_name varchar(128),
    invite varchar(20),
    username varchar(32),

    primary key (channel_id)
);

create table posts
(

    channel_id bigint not null,
    source_id      int not null,
    post_id        int not null,
    backup_id int not null,
    reply_id int,
    media_id bigint,

    primary key (channel_id, source_id),
    CONSTRAINT fk_channel
      FOREIGN KEY(channel_id)
	  REFERENCES sources(channel_id)
);