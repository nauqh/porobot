"""Configuration

This module contains settings from environment variables, 
validate and raise error if not found.

"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8')

    TOKEN: str
    GUILD: int
    STDOUT_CHANNEL_ID: int

    RIOT: str


settings = Settings()
