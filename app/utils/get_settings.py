from app.config.fastapi import FastapiSettings
from app.config.mongo import MongoSettings
from app.config.postgres import PostgresSettings


def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()


def get_mongo_settings() -> MongoSettings:
    return MongoSettings()


def get_fastapi_settings() -> FastapiSettings:
    return FastapiSettings()
