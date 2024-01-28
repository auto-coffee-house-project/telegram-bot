from models import Invitation
from views.base import TextView

__all__ = ('InvitationView',)


class InvitationView(TextView):

    def __init__(self, bot_username: str, invitation: Invitation):
        self.__bot_username = bot_username
        self.__invitation = invitation

    def get_text(self) -> str:
        url = (
            f'https://t.me/{self.__bot_username}?'
            f'start=invite-{self.__invitation.id.hex}'
        )
        return f'Ссылка-приглашение: {url}'
