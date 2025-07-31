import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    bot_token: str
    channel_id: str
    channel_url: str
    contact_phone: str
    contact_username: str


def load_config(path: str | None = None) -> Config:
    load_dotenv(path)
    return Config(
        bot_token=os.getenv("BOT_TOKEN"),
        channel_id=os.getenv("CHANNEL_ID"),
        channel_url=os.getenv("CHANNEL_URL"),
        contact_phone=os.getenv("CONTACT_PHONE"),
        contact_username=os.getenv("CONTACT_USERNAME"),
    )
