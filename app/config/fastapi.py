from pydantic import BaseSettings

class FastapiSettings(BaseSettings):
    FASTAPI_SECRET: str
    FASTAPI_HASH_ALGORITHM: str
    FASTAPI_HASH_EXPIRATION: int

    class Config:
        env_file: str = '.env'