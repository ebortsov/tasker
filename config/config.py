from dataclasses import dataclass
from environs import Env
from pathlib import Path


@dataclass
class TelegramBot:
    token: str


@dataclass
class Databases:
    history_of_users_tasks: Path


@dataclass
class Config:
    def __init__(self, env_path: str | None = None):
        env = Env()
        env.read_env(path=env_path)

        self.telegram_bot = TelegramBot(token=env.str('TOKEN'))
        test_path = env.str('HISTORY_OF_USERS_TASKS')
        self.databases = Databases(history_of_users_tasks=Path(env.str('HISTORY_OF_USERS_TASKS')))
