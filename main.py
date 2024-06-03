from aiogram import Bot
from aiogram import Dispatcher

from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import logging
import asyncio

from config.config import Config
from middlewares.check_active_middleware import CheckActiveMiddleware
from handlers import common_handlers
from handlers import tasks_handlers
from lexicon.simple_lexicion import DefaultLexicon


async def main():
    logging.basicConfig(level=logging.DEBUG)
    config = Config()

    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(CheckActiveMiddleware())
    dp.include_router(common_handlers.router)
    dp.include_router(tasks_handlers.router)

    dp.workflow_data.update(lexicon=DefaultLexicon)

    bot = Bot(
        token=config.telegram_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    await bot.delete_my_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
