CREATE DATABASE sdl_db
    WITH OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'ru_RU.UTF-8'
    LC_CTYPE = 'ru_RU.UTF-8'
    TEMPLATE = template0;

CREATE ROLE laba_user WITH LOGIN PASSWORD 'password';

GRANT CONNECT ON DATABASE sdl_db TO laba_user;

\connect sdl_db

GRANT USAGE ON SCHEMA public TO laba_user;
