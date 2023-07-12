from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Validate env variables, raise error if not found 
    """
    TOKEN: str
    GUILD: int
    STDOUT_CHANNEL_ID: int
    VOICE_CHANNEL_ID: int
    RIOT: str

    class Config():
        env_file = ".env"


settings = Settings()
