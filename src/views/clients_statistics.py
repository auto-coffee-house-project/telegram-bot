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
            '<b>ID клиента | Общее количество чашек | Бесплатные чашки</b>',
        ]

        for client_statistics in self.__clients_statistics:
            lines.append(
                f'{client_statistics.user_id}'
                f' | {client_statistics.total_purchases_count} шт.'
                f' | {client_statistics.free_purchases_count} шт.'
            )

        return '\n'.join(lines)
