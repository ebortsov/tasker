from dataclasses import dataclass
from environs import Env


@dataclass
class TelegramBot:
    token: str


@dataclass
class Config:
    def __init__(self, env_path: str | None = None):
        env = Env()
        env.read_env(path=env_path)

        self.telegram_bot = TelegramBot(
            token=env.str('TOKEN')
        )
