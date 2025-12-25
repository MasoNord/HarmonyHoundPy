import logging
import os
from dataclasses import dataclass
from logging import getLogger
from dotenv import load_dotenv
from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

BOT_TOKEN_ENV = "BOT_TOKEN"

DB_USER_ENV = "DB_USER"
DB_PASSWORD_ENV = "DB_PASSWORD"
DB_HOST_ENV = "DB_HOST_ENV"
DB_NAME_ENV = "DB_NAME_ENV"
DB_PORT_ENV = "DB_PORT"
BOT_ADMIN_IDS_ENV = "BOT_ADMIN_IDS"
RAPID_API_KEY = "RAPID_API_KEY"
RAPID_API_HOST = "RAPID_API_HOST"

logger = getLogger(__name__)
load_dotenv()

class ConfigParseError(ValueError):
    pass

@dataclass
class RapidApiConfig:
    rapid_api_key: str
    rapid_api_host: str

@dataclass
class BotConfig:
    bot_token: str
    admin_ids: int

@dataclass
class DatabaseConfig:
    db_user: str
    db_password: str
    db_host: str
    db_name: str
    db_port: str

    def get_db_url(self):
        return (f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")


def get_str_env(key) -> str:
    val = os.getenv(key)

    if not val:
        logger.error("%s is not set", key)
        raise ConfigParseError(f"{key} is not set")

    return val

def load_bot_config() -> BotConfig:
    logger.info("Reading bot config from .env file")

    bot_token = get_str_env(BOT_TOKEN_ENV)
    admin_ids = get_str_env(BOT_ADMIN_IDS_ENV)

    return BotConfig(
        bot_token=bot_token,
        admin_ids=int(admin_ids)
    )

def load_rapid_api_config() -> RapidApiConfig:
    logger.info("Reading rapid api config from .env file")

    rapid_api_key = get_str_env(RAPID_API_KEY)
    rapid_api_host = get_str_env(RAPID_API_HOST)

    return RapidApiConfig(
        rapid_api_key=rapid_api_key,
        rapid_api_host=rapid_api_host
    )

def load_database_config() -> DatabaseConfig:
    db_user = get_str_env(DB_USER_ENV)
    db_password = get_str_env(DB_PASSWORD_ENV)
    db_host = get_str_env(DB_HOST_ENV)
    db_name = get_str_env(DB_NAME_ENV)
    db_port = get_str_env(DB_PORT_ENV)

    return DatabaseConfig(
        db_user=db_user,
        db_password=db_password,
        db_host=db_host,
        db_name=db_name,
        db_port=db_port
    )

bot_config = load_bot_config()

bot = Bot(token=bot_config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
admins = bot_config.admin_ids

logging.basicConfig(level=logging.INFO)