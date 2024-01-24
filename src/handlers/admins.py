from aiogram import Router, F, Bot
from aiogram.filters import StateFilter
from aiogram.types import Message

from exceptions import AdminDoesNotExistError
from repositories import InvitationRepository

__all__ = ('router',)

from views import answer_view

from views.invitations import InvitationView

router = Router(name=__name__)


@router.message(
    F.text == '🔗 Ссылка-приглашение',
    StateFilter('*'),
)
async def on_create_invitation(
        message: Message,
        bot: Bot,
        invitation_repository: InvitationRepository,
) -> None:
    try:
        invitation = await invitation_repository.create(message.from_user.id)
    except AdminDoesNotExistError:
        await message.reply('Вы не являетесь администратором')
        return
    bot_user = await bot.get_me()
    view = InvitationView(bot_username=bot_user.username, invitation=invitation)
    await answer_view(message, view)


