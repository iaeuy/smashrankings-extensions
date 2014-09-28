drop table if exists playerdata;
create table playerdata (
    name text not null,
    data blob not null
);