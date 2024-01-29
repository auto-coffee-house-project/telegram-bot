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
import models
from config import load_config_from_file
from logger import setup_config
from middlewares import (
    APIRepositoriesInitializerMiddleware,
    HttpClientInitializerMiddleware,
    user_middleware,
)
from repositories import (
    BotRepository,
    UserRepository,
    SalesmanRepository,
    ShopGroupRepository,
    InvitationRepository,
    AdminRepository,
    MailingRepository,
)
from repositories.sales import SaleRepository


def register_routers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        handlers.invitations.router,
        handlers.salesmans.router,
        handlers.codes.router,
        handlers.start.router,
        handlers.mailings.router,
        handlers.errors.router,
    )


async def setup_web_app_menu_buttons(
        *,
        bots: Iterable[models.Bot],
        web_app_url: str,
) -> None:
    for bot in bots:
        url = f'{web_app_url.rstrip("/")}?botId={bot.id}&botUsername={bot.username}'
        bot = Bot(token=bot.token)
        menu_button = MenuButtonWebApp(
            text='Get Coffee',
            web_app=WebAppInfo(url=url),
        )
        await bot.set_chat_menu_button(menu_button=menu_button)


async def main() -> None:
    root_path = pathlib.Path(__file__).parent.parent
    config_file_path = root_path / 'config.toml'
    config = load_config_from_file(config_file_path)

    logging_config_file_path = root_path / 'logging_config.json'
    setup_config(logging_config_file_path)

    dispatcher = Dispatcher(storage=MemoryStorage())

    register_routers(dispatcher)

    http_client_factory = partial(
        httpx.AsyncClient,
        base_url=config.api_base_url,
    )

    async with http_client_factory() as http_client:
        bot_repository = BotRepository(http_client)
        bots = await bot_repository.get_all()

    await setup_web_app_menu_buttons(
        bots=bots,
        web_app_url=config.web_app_url,
    )
    bots = [Bot(token=bot.token, parse_mode=ParseMode.HTML) for bot in bots]

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
            invitation_repository=InvitationRepository,
            admin_repository=AdminRepository,
            mailing_repository=MailingRepository,
        ),
    )
    dispatcher.update.outer_middleware(user_middleware)

    await dispatcher.start_polling(*bots)


if __name__ == '__main__':
    asyncio.run(main())
