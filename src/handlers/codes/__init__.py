from aiogram import Router

from . import manual_input, deep_link, cancel_sale

__all__ = ('router',)

router = Router(name=__name__)

router.include_routers(
    deep_link.router,
    manual_input.router,
    cancel_sale.router,
)
