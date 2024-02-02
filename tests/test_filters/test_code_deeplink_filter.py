from dataclasses import dataclass

import pytest

from filters import code_deeplink_filter


@dataclass(frozen=True, slots=True)
class Message:
    text: str


@pytest.mark.parametrize(
    'deeplink',
    [
        '/start scanuser:1234',
        '/startscan-user:123',
        '/start scan-user:',
        '/start scan-user:abcd',
    ],
)
def test_deeplink_invalid_structure(deeplink: str) -> None:
    assert not code_deeplink_filter(Message(deeplink))


@pytest.mark.parametrize(
    'deeplink, expected_code',
    [
        ('/start scan-user:54545454545', 54545454545),
        ('/start scan-user:12345', 12345),
        ('/start scan-user:-1234567', -1234567),
    ],
)
def test_deeplink_valid_structure(deeplink: str, expected_code: int) -> None:
    expected = {'client_user_id': expected_code}
    assert code_deeplink_filter(Message(deeplink)) == expected
