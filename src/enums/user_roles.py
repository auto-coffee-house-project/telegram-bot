from enum import StrEnum, auto

__all__ = ('UserRole',)


class UserRole(StrEnum):
    ADMIN = auto()
    CLIENT = auto()
    SALESMAN = auto()
