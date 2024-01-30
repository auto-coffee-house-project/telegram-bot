from collections.abc import Iterable

from models import ClientPurchasesStatistics
from views.base import TextView

__all__ = ('ClientsStatisticsView',)


class ClientsStatisticsView(TextView):

    def __init__(self, clients_statistics: Iterable[ClientPurchasesStatistics]):
        self.__clients_statistics = tuple(clients_statistics)

    def get_text(self) -> str:
        if not self.__clients_statistics:
            return '😔 Ваши клиенты пока не сделали ни одной покупки'

        lines: list[str] = [
            '<b>Имя клиента | Общее количество чашек | Бесплатные чашки</b>',
        ]

        for client_statistics in self.__clients_statistics:
            name = (
                    client_statistics.user.username
                    or client_statistics.user.full_name
            )
            lines.append(
                f'{name}'
                f' | {client_statistics.total_purchases_count} шт.'
                f' | {client_statistics.free_purchases_count} шт.'
            )

        return '\n'.join(lines)
