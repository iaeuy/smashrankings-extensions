drop table if exists playerdata;
create table playerdata (
    name text primary key,
    data blob not null
);