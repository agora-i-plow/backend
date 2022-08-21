from pydantic import BaseSettings


class MongoSettings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str
    MONGO_HOST: str

    class Config:
        env_file: str = ".env"

    @property
    def db_uri(self) -> str:
        return f"mongodb://{self.MONGO_USER}:{self.MONGO_PASSWORD}@{self.MONGO_HOST}"
