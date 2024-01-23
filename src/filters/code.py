from aiogram.types import Message

__all__ = ('code_input_filter', 'code_deeplink_filter')


def validate_code(code: str) -> bool | dict:
    if len(code) != 4:
        return False

    if not code.isdigit():
        return False

    return {'code': code}


def code_deeplink_filter(message: Message) -> bool | dict:
    if not message.text.startswith('/start scan-'):
        return False
    try:
        code = message.text.split('-')[1]
    except IndexError:
        return False
    return validate_code(code)


def code_input_filter(message: Message) -> bool | dict:
    return validate_code(message.text)
