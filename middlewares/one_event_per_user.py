"""
This middleware implements the protection from simultaneous execution of several events for the same user.
"""

import logging

from aiogram import BaseMiddleware

active_users = set()


class OneEventPerUser(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = data["event_from_user"]
        if user_id not in active_users:
            logging.debug("Allow event")
            active_users.add(user_id)
            try:
                await handler(event, data)
            except Exception as e:
                raise e  # Ignore exceptions (the latter middleware will catch them)
            finally:
                active_users.remove(user_id)
        else:
            logging.debug("Do not allow event")
