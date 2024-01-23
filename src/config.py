import pathlib
import tomllib
from dataclasses import dataclass

__all__ = ('Config', 'load_config_from_file')


@dataclass(frozen=True, slots=True)
class Config:
    api_base_url: str


def load_config_from_file(file_path: pathlib.Path) -> Config:
    config_text = file_path.read_text(encoding='utf-8')
    config = tomllib.loads(config_text)
    return Config(
        api_base_url=config['api_base_url'],
    )
