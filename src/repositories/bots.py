from repositories.base import APIRepository

__all__ = ('BotRepository',)


class BotRepository(APIRepository):

    async def get_all(self) -> list[dict]:
        url = '/telegram/bots/'
        response = await self._http_client.get(url)
        # TODO check response
        return response.json()
