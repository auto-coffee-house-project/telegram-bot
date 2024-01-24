__all__ = ('BotDoesNotExistError',)


class BotDoesNotExistError(Exception):
    """Raised when a bot does not exist."""

    def __init__(self, bot_id: int):
        self.bot_id = bot_id
