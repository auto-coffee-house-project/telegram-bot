from uuid import UUID

from aiogram.types import Message

__all__ = ('invitation_deeplink_filter',)


def invitation_deeplink_filter(message: Message) -> bool | dict:
    if not message.text.startswith('/start invite-'):
        return False
    try:
        invitation_id = message.text.split('-')[1]
    except IndexError:
        return False

    try:
        invitation_id = UUID(invitation_id)
    except ValueError:
        return False

    return {'invitation_id': invitation_id}
