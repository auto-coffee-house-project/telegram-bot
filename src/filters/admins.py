from aiogram.types import Message

from exceptions import AdminDoesNotExistError
from repositories import AdminRepository

__all__ = ('admin_filter',)


async def admin_filter(
        message: Message,
        admin_repository: AdminRepository,
) -> bool | dict:
    user_id = message.from_user.id
    try:
        admin = await admin_repository.get_by_user_id(user_id)
    except AdminDoesNotExistError:
        return False
    return {'admin': admin}
