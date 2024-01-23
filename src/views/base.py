from typing import TypeAlias

from aiogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ForceReply,
    ReplyKeyboardRemove,
    Message,
)

__all__ = (
    'ReplyMarkup',
    'TextView',
    'PhotoView',
    'answer_view',
    'answer_photo_view',
)

ReplyMarkup: TypeAlias = (
        ReplyKeyboardMarkup
        | InlineKeyboardMarkup
        | ForceReply
        | ReplyKeyboardRemove
)


class TextView:
    text: str | None = None
    reply_markup: ReplyMarkup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> ReplyMarkup | None:
        return self.reply_markup


class PhotoView:
    caption: str | None = None
    photo: str

    def get_caption(self) -> str | None:
        return self.caption

    def get_photo(self) -> str:
        return self.photo


async def answer_view(message: Message, view: TextView) -> Message:
    return await message.answer(
        text=view.get_text(),
        reply_markup=view.get_reply_markup(),
    )


async def answer_photo_view(message: Message, view: PhotoView) -> Message:
    return await message.answer_photo(
        photo=view.photo,
        caption=view.caption,
    )
