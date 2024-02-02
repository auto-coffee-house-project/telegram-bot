from typing import Protocol

__all__ = ('code_input_filter', 'code_deeplink_filter')


class HasText(Protocol):
    text: str


def code_deeplink_filter(message: HasText) -> bool | dict:
    if not message.text.startswith('/start scan-user_'):
        return False

    user_id = message.text.split('_')[-1]

    try:
        user_id = int(user_id)
    except ValueError:
        return False

    return {'client_user_id': user_id}


def code_input_filter(message: HasText) -> bool | dict:
    code = message.text

    if len(code) != 4:
        return False

    if not code.isdigit():
        return False

    return {'code': code}
