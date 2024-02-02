from dataclasses import dataclass

import pytest

from filters import code_deeplink_filter


@dataclass(frozen=True, slots=True)
class Message:
    text: str


@pytest.mark.parametrize(
    'deeplink',
    [
        '/start scanuser_1234',
        '/startscan-user_123',
        '/start scan-user_',
        '/start scan-user_abcd',
    ],
)
def test_deeplink_invalid_structure(deeplink: str) -> None:
    assert not code_deeplink_filter(Message(deeplink))


@pytest.mark.parametrize(
    'deeplink, expected_code',
    [
        ('/start scan-user_54545454545', 54545454545),
        ('/start scan-user_12345', 12345),
        ('/start scan-user_-1234567', -1234567),
    ],
)
def test_deeplink_valid_structure(deeplink: str, expected_code: int) -> None:
    expected = {'client_user_id': expected_code}
    assert code_deeplink_filter(Message(deeplink)) == expected
