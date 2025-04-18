from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.session.middlewares.request_logging import logger
from loader import bot
from utils.db.alchemy import create_user
from keyboards.inline.home_buttons import home_key
router = Router()


@router.message(CommandStart())
async def do_start(message: types.Message):
    # telegram_id = message.from_user.id
    # full_name = message.from_user.full_name
    # username = message.from_user.username
    create_user(cid=message.chat.id)
    await message.answer(f"Quyidagilardan birini tanlang! 👇",reply_markup=home_key)
