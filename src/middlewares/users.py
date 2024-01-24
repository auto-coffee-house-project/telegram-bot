from aiogram.types import Update

from middlewares.common import HandlerReturn, Handler, ContextData
from repositories import UserRepository


async def user_middleware(
        handler: Handler,
        event: Update,
        data: ContextData,
) -> HandlerReturn:
    message_or_callback_query = event.message or event.callback_query
    if message_or_callback_query is not None:
        user = message_or_callback_query.from_user
        user_repository: UserRepository = data['user_repository']
        await user_repository.upsert_user(user)
    return await handler(event, data)
