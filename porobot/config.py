"""Configuration

This module contains settings from environment variables, 
validate and raise error if not found.

"""

from pydantic import BaseSettings


class Settings(BaseSettings):
    TOKEN: str
    GUILD: int
    STDOUT_CHANNEL_ID: int
    VOICE_CHANNEL_ID: int
    RIOT: str

    class Config():
        env_file = ".env"


settings = Settings()
