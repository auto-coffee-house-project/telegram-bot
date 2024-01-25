import json
import logging
import logging.config
import pathlib
import time

__all__ = ('setup_config',)


class UTCFormatter(logging.Formatter):
    converter = time.gmtime


def setup_config(file_path: pathlib.Path) -> None:
    if not file_path.exists():
        print('Logging config file not found')
        exit(1)

    if not file_path.name.endswith('.json'):
        print('Logging config file must be a JSON file')
        exit(1)

    config_json = file_path.read_text('utf-8')

    try:
        config = json.loads(config_json)
    except json.JSONDecodeError:
        print('Logging config file is not a valid JSON file')
        exit(1)

    logging.config.dictConfig(config)
