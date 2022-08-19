create extension if not exists "uuid-ossp";
create type roles as enum ('admin','producer');
create table if not exists users(
    uuid uuid primary key default uuid_generate_v4(),
    username text unique not null,
    hashed_password text not null,
    role roles default 'producer'
);