create table candidate (
    name        text primary key,
);

create table tweet (
    id          integer primary key autoincrement not null,
    time        date,
    sentiment   float,
    text        text,
    coordinates text,
    favorites   integer,
    retweets    integer,
    candidate   text not null references candidate(name),
);
