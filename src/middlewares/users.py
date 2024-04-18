from aiogram import Bot
from aiogram.types import Update

from middlewares.common import HandlerReturn, Handler, ContextData
from repositories import UserRepository


async def user_middleware(
        handler: Handler,
        event: Update,
        data: ContextData,
) -> HandlerReturn:
    message_or_callback_query = event.message or event.callback_query
    from_user = message_or_callback_query.from_user
    if message_or_callback_query is not None:
        user_repository: UserRepository = data['user_repository']
        user = await user_repository.upsert_user(user=from_user)
        data['user'] = user
    return await handler(event, data)
