from collections.abc import Callable
from contextlib import AbstractAsyncContextManager
from typing import TypeAlias

import httpx
from aiogram import BaseMiddleware, Bot
from aiogram.types import Update

from middlewares.common import Handler, ContextData, HandlerReturn

__all__ = ('HttpClientInitializerMiddleware',)

HttpClientFactory: TypeAlias = (
    Callable[..., AbstractAsyncContextManager[httpx.AsyncClient]]
)


class HttpClientInitializerMiddleware(BaseMiddleware):

    __slots__ = ('__closing_http_client_factory',)

    def __init__(self, closing_http_client_factory: HttpClientFactory):
        self.__closing_http_client_factory = closing_http_client_factory

    async def __call__(
            self,
            handler: Handler,
            event: Update,
            data: ContextData,
    ) -> HandlerReturn:
        bot: Bot = data['bot']
        headers = {'bot-id': str(bot.id)}

        async with self.__closing_http_client_factory(
                headers=headers,
        ) as http_client:
            data['http_client'] = http_client

            return await handler(event, data)
