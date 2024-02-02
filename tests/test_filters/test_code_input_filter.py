from dataclasses import dataclass

import pytest

from filters import code_input_filter


@dataclass(frozen=True, slots=True)
class Message:
    text: str


@pytest.mark.parametrize(
    'code',
    [
        '12345',
        '123',
        '12364',
        '0123124543',
    ],
)
def test_code_length_not_4(code: str):
    assert not code_input_filter(Message(code))


@pytest.mark.parametrize(
    'code',
    [
        'a123',
        '1a23',
        'aaaa',
        'aF13',
    ],
)
def test_code_contains_non_digits(code: str):
    assert not code_input_filter(Message(code))


def test_code_empty_string():
    assert not code_input_filter(Message(''))


@pytest.mark.parametrize(
    'code',
    [
        '1234',
        '0000',
        '9999',
    ],
)
def test_code_valid(code: str):
    assert code_input_filter(Message(code)) == {'code': code}
