import asyncio
import pathlib
from collections.abc import Iterable
from functools import partial

import httpx
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import MenuButtonWebApp, WebAppInfo

import handlers
from config import load_config_from_file
from middlewares import (
    APIRepositoriesInitializerMiddleware,
    HttpClientInitializerMiddleware,
)
from repositories import (
    BotRepository,
    UserRepository,
    SalesmanRepository,
    ShopGroupRepository,
)
from repositories.sales import SaleRepository


def register_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.scan.router,
        handlers.start.router,
        handlers.code_input.router,
        handlers.errors.router,
    )


async def setup_web_app_menu_buttons(
        *,
        bots: Iterable[Bot],
        web_app_url: str,
) -> None:
    menu_button = MenuButtonWebApp(
        text='Get Coffee',
        web_app=WebAppInfo(url=web_app_url),
    )
    for bot in bots:
        await bot.set_chat_menu_button(menu_button=menu_button)


async def main() -> None:
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config_from_file(config_file_path)

    dispatcher = Dispatcher(storage=MemoryStorage())

    register_routers(dispatcher)

    http_client_factory = partial(
        httpx.AsyncClient,
        base_url=config.api_base_url,
    )

    async with http_client_factory() as http_client:
        bot_repository = BotRepository(http_client)
        bots = await bot_repository.get_all()

    bots = [Bot(token=bot.token, parse_mode=ParseMode.HTML) for bot in bots]

    await setup_web_app_menu_buttons(
        bots=bots,
        web_app_url=config.web_app_url,
    )

    dispatcher.update.outer_middleware(
        HttpClientInitializerMiddleware(http_client_factory),
    )
    dispatcher.update.outer_middleware(
        APIRepositoriesInitializerMiddleware(
            bot_repository=BotRepository,
            sale_repository=SaleRepository,
            salesman_repository=SalesmanRepository,
            user_repository=UserRepository,
            shop_group_repository=ShopGroupRepository,
        ),
    )

    await dispatcher.start_polling(*bots)


if __name__ == '__main__':
    asyncio.run(main())
