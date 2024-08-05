import logging
import sys
from dataclasses import dataclass
from pathlib import Path

from environs import Env


@dataclass
class TelegramBot:
    token: str


@dataclass
class Databases:
    database: Path


@dataclass
class LoggingConfig:
    path_to_warning_logs: Path


@dataclass
class Config:
    def __init__(self, env_path: str | None = None):
        env = Env()
        env.read_env(path=env_path)

        self.logging_config = LoggingConfig(
            path_to_warning_logs=env.str("WARNING_LOGS")
        )
        self.telegram_bot = TelegramBot(token=env.str("TOKEN"))
        self.databases = Databases(database=Path(env.str("DATABASE")))


def logging_config():
    logger_format = (
        "%(levelname)s [%(asctime)s] - %(filename)s:%(lineno)d - %(name)s - %(message)s"
    )
    default_formatter = logging.Formatter(fmt=logger_format)

    default_handler = logging.StreamHandler(sys.stderr)
    default_handler.setLevel(level=logging.WARNING)
    default_handler.setFormatter(fmt=default_formatter)

    config = Config()

    warning_handler = logging.FileHandler(
        filename=config.logging_config.path_to_warning_logs, mode="a", encoding="utf-8"
    )
    warning_handler.setLevel(level=logging.WARNING)
    warning_handler.setFormatter(fmt=default_formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(default_handler)
    root_logger.addHandler(warning_handler)

    root_logger.setLevel(level=logging.DEBUG)
