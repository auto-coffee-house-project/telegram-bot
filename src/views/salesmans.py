from models import SalesmanCreateResponse
from views import TextView

__all__ = ('SalesmanCreatedView',)


class SalesmanCreatedView(TextView):

    def __init__(self, salesman_created: SalesmanCreateResponse):
        self.__salesman_created = salesman_created

    def get_text(self) -> str:
        return (
            'Вы теперь продавец в кофейне'
            f' {self.__salesman_created.shop_name}'
        )
