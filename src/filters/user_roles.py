from functools import partial

from enums import UserRole
from models import User

__all__ = (
    'user_is_admin_filter',
    'user_is_client_filter',
    'user_is_salesman_filter',
)


def user_role_filter(*args, user: User, user_role: UserRole) -> bool:
    return user.role == user_role


user_is_admin_filter = partial(user_role_filter, user_role=UserRole.ADMIN)
user_is_client_filter = partial(user_role_filter, user_role=UserRole.CLIENT)
user_is_salesman_filter = partial(user_role_filter, user_role=UserRole.SALESMAN)
