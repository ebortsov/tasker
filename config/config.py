import logging
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
    path_to_other_logs: Path


@dataclass
class Config:
    def __init__(self):
        env = Env()

        self.logging_config = LoggingConfig(
            path_to_warning_logs=env.str('WARNING_LOGS'), path_to_other_logs=env.str('LOGS')
        )
        self.telegram_bot = TelegramBot(token=env.str('TOKEN'))
        self.databases = Databases(database=Path(env.str('DATABASE')))


def logging_config():
    logger_format = '%(levelname)s [%(asctime)s] - %(filename)s:%(lineno)d - %(name)s - %(message)s'
    default_formatter = logging.Formatter(fmt=logger_format)

    config = Config()

    default_handler = logging.FileHandler(
        filename=config.logging_config.path_to_other_logs, mode='a', encoding='utf-8'
    )
    default_handler.setLevel(level=logging.INFO)
    default_handler.setFormatter(fmt=default_formatter)

    warning_handler = logging.FileHandler(
        filename=config.logging_config.path_to_warning_logs, mode='a', encoding='utf-8'
    )
    warning_handler.setLevel(level=logging.WARNING)
    warning_handler.setFormatter(fmt=default_formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(default_handler)
    root_logger.addHandler(warning_handler)

    root_logger.setLevel(level=logging.DEBUG)
