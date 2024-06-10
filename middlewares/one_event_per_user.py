"""
Due to the asynchronous nature of aiogram, several messages sent with very small delay (for example, when Telegram
splits long messages) may result in the situation when some handler will be launched several times for the same user.
Sometimes we want to prevent such behavior. This middlewares addresses this exact issue.
"""
from aiogram import BaseMiddleware
from collections import defaultdict
import logging

has_active_event = defaultdict(lambda: False)


class OneEventPerUser(BaseMiddleware):
    async def __call__(self, handler, event, data):
        user_id = data['event_from_user']
        if not has_active_event[user_id]:
            logging.debug('Allow event')
            has_active_event[user_id] = True
            result = await handler(event, data)
            has_active_event[user_id] = False
            return result
        else:
            logging.debug('Do not allow event')

