from aiogram import Router

from . import manual_input, deep_link, delete

__all__ = ('router',)

router = Router(name=__name__)

router.include_routers(
    deep_link.router,
    manual_input.router,
    delete.router,
)
