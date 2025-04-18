from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Any, Dict
from aiogram.types import Message, CallbackQuery
from loader import bot
from utils.db.alchemy import get_channel
from keyboards.inline.buttons import join_buttons


class SubscriptionMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        channels = get_channel()

        x_channels = []

        for channel in channels:
            status = await event.bot.get_chat_member(
                chat_id=channel, user_id=event.from_user.id
            )
            if status.status == "left":
                x_channels.append(await bot.export_chat_invite_link(chat_id=channel))
        if len(x_channels) > 0:
            await event.answer(
                text="Iltimos, barcha kanallarga obuna bo'ling!",
                reply_markup=join_buttons(x_channels),
            )
            return
        return await handler(event, data)


class SubscriptionMiddlewareCallback(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        channels = get_channel()
        x_channels = []

        for channel in channels:
            status = await bot.get_chat_member(
                chat_id=channel, user_id=event.from_user.id
            )
            if status.status == "left":
                x_channels.append(await bot.export_chat_invite_link(chat_id=channel))

        if x_channels:
            await event.message.answer(
                text="Iltimos, barcha kanallarga obuna bo'ling!",
                reply_markup=join_buttons(x_channels),
            )
            return
        return await handler(event, data)
