from aiogram.types import Message

from exceptions import SalesmanDoesNotExistError
from repositories import SalesmanRepository

__all__ = ('salesman_filter',)


async def salesman_filter(
        message: Message,
        salesman_repository: SalesmanRepository,
) -> bool | dict:
    user_id = message.from_user.id
    try:
        salesman = await salesman_repository.get_by_user_id(user_id)
    except SalesmanDoesNotExistError:
        return False
    return {'salesman': salesman}
