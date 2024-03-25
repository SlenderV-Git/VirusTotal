from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class BotSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive= False
    )
    
    bot_token : str
    api_token : str
 
def load_settings() -> BotSettings:
    return BotSettings()