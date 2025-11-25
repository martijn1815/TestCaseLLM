from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv(".env"))


class Settings(BaseSettings):
    port: int
    host_url: str
    api_key: str
    model: str

    class Config:
        env_file = ".env"


settings = Settings()
