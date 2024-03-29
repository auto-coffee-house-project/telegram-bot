import contextlib

from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

from models import Sale
from views import CodeSuccessfullyAppliedNotificationForClientView

__all__ = ('send_code_applied_notification',)


async def send_code_applied_notification(
        bot: Bot,
        sale: Sale,
) -> None:
    view = CodeSuccessfullyAppliedNotificationForClientView(sale)
    with contextlib.suppress(TelegramAPIError):
        await bot.send_message(
            chat_id=sale.client_user_id,
            text=view.get_text(),
            reply_markup=view.get_reply_markup(),
        )
