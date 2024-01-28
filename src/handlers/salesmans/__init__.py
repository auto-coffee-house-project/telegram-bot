from aiogram import Router

from . import list, delete

__all__ = ('router',)

router = Router(name=__name__)
router.include_routers(
    list.router,
    delete.router,
)
