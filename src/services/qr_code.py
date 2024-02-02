import urllib.parse

__all__ = ('build_bonus_deeplink', 'create_qr_code')


def build_bonus_deeplink(
        *,
        bot_username: str,
        user_id: int,
) -> str:
    return f'https://t.me/{bot_username}?start=scan-user_{user_id}'


def create_qr_code(data: str) -> str:
    query_params = {
        'size': '450x450',
        'data': data,
    }
    encoded_query_params = urllib.parse.urlencode(query_params)
    return (
        f'https://api.qrserver.com/v1/create-qr-code/?{encoded_query_params}'
    )
