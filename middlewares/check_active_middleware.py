"""
This middleware checks if the user has called the command /start
In case of the user did not call the /start, the middleware replies to the message
Additionally, this middleware provides protection from the project to fall because of some exceptions
Attach this middleware to the updates to the Dispatcher class
"""

import logging
from typing import Any

from aiogram import BaseMiddleware

from lexicon.simple_lexicion import DefaultLexicon

# active_users is a set of users (user ids) which called the command /start
active_users: set[int] = set()

# Set of user ids for which the bot for some reason raised the exception
error_occurred: set[int] = set()


class CheckActiveMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict[str, Any]):
        user_id = data["event_from_user"]
        lexicon: DefaultLexicon = data["lexicon"]

        # This concrete update is a command '/start <args>'
        if event.message is not None and event.message.text == "/start":
            if user_id in error_occurred:
                error_occurred.remove(user_id)
            active_users.add(user_id)

        # The user called command /start
        if user_id in active_users:
            try:
                await handler(event, data)
            except Exception as e:
                logging.error(e)
                active_users.remove(user_id)
                error_occurred.add(user_id)
            return

        # Otherwise, if the update is message reply to the user
        if event.message is not None:
            await event.message.answer(
                lexicon.msg_restart_the_bot_because_of_error
                if user_id in error_occurred
                else lexicon.msg_use_start
            )
