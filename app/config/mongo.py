from pydantic import BaseSettings, PostgresDsn

class MongoSettings(BaseSettings):
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_DATABASE: str
    MONGO_HOST: str

    class Config:
        env_file: str = '.env'

    # @property
    # def db_uri(self) -> str:
    #     return PostgresDsn.build(
    #         scheme="mongo",
    #         user=self.MONGO_USER,
    #         password=self.MONGO_PASSWORD,
    #         host=self.MONGO_HOST,
    #         path=f'/{self.MONGO_DATABASE}',
    #     )
