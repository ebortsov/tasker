"""
This middleware implements the protection from simultaneous execution of several events for the same user.
"""
from aiogram import BaseMiddleware
from collections import defaultdict
import logging

active_users = set()


class OneEventPerUser(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = data['event_from_user']
        if user_id not in active_users:
            logging.debug('Allow event')
            active_users.add(user_id)
            result = await handler(event, data)
            active_users.remove(user_id)
            return result
        else:
            logging.debug('Do not allow event')

