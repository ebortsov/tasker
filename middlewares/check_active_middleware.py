"""
This middleware checks if the user has called the command /start
In case of the user did not call the /start, the middleware replies to the message
Attach this middleware to the updates to the Dispatcher class
"""
from aiogram import BaseMiddleware
from aiogram import types
from typing import Any
import logging

# active_users is a set of users (user ids) which called the command /start
active_users: set[int] = set()


class CheckActiveMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict[str, Any]):
        user_id = data['event_from_user']
        # This concrete update is a command '/start'
        if hasattr(event, 'message') and event.message.text.startswith('/start'):
            active_users.add(user_id)

        # The user called command /start
        if user_id in active_users:
            return await handler(event, data)

        # Otherwise, if the update is message reply to the user
        if hasattr(event, 'message'):
            await event.message.answer('Please, use the command /start to start the bot')

