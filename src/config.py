from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    BOT_NAME: str


settings = Settings(_env_file=".env")