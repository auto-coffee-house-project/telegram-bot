__all__ = ('CodeDoesNotExistError', 'CodeExpiredError')


class CodeDoesNotExistError(Exception):

    def __init__(self, code):
        self.code = code


class CodeExpiredError(Exception):

    def __init__(self, code):
        self.code = code
