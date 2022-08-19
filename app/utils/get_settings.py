from app.config.postgres import PostgresSettings
from app.config.mongo import MongoSettings
from app.config.fastapi import FastapiSettings

def get_postgres_settings() -> PostgresSettings:
    return PostgresSettings()

def get_mongo_settings() -> MongoSettings:
    return MongoSettings()

def get_fastapi_settings() -> FastapiSettings:
    return FastapiSettings()