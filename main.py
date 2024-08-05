import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config import Config, logging_config
from db import db_common
from handlers import common_handlers, edit_task_handlers, tasks_handlers
from handlers.pagination import view_tasks_handlers
from handlers.utc_offset_update import update_utc
from lexicon.simple_lexicion import DefaultLexicon
from middlewares.check_active_middleware import CheckActiveMiddleware
from middlewares.one_event_per_user import OneEventPerUser


async def main():
    config = Config()
    logging_config()  # Configure logging settings
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(CheckActiveMiddleware())
    dp.update.middleware(OneEventPerUser())

    dp.include_router(common_handlers.router)
    dp.include_router(tasks_handlers.router)
    dp.include_router(view_tasks_handlers.router)
    dp.include_router(edit_task_handlers.router)
    dp.include_router(update_utc.router)

    dp.workflow_data.update(lexicon=DefaultLexicon)

    # Setting up database
    db_conn = db_common.get_connection()
    db_common.init(db_conn)
    dp.workflow_data.update(db_conn=db_conn)

    bot = Bot(
        token=config.telegram_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await bot.delete_my_commands()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
