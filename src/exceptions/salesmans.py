__all__ = (
    'SalesmanDoesNotExistError',
    'SalesmanAndSaleCodeShopGroupsNotEqualError',
    'SalesmanAlreadyExistsError',
)


class SalesmanDoesNotExistError(Exception):

    def __init__(self, salesman_user_id: int):
        self.salesman_user_id = salesman_user_id


class SalesmanAndSaleCodeShopGroupsNotEqualError(Exception):

    def __init__(self, salesman_user_id: int, code: str):
        self.salesman_user_id = salesman_user_id
        self.code = code


class SalesmanAlreadyExistsError(Exception):
    """Raised when user is already a salesman."""
