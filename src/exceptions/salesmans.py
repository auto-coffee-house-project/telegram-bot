__all__ = (
    'SalesmanDoesNotExistError',
    'SalesmanAndSaleCodeShopGroupsNotEqualError',
)


class SalesmanDoesNotExistError(Exception):

    def __init__(self, salesman_user_id: int):
        self.salesman_user_id = salesman_user_id


class SalesmanAndSaleCodeShopGroupsNotEqualError(Exception):

    def __init__(self, salesman_user_id: int, code: str):
        self.salesman_user_id = salesman_user_id
        self.code = code
