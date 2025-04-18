from aiogram import Router, types, F
from keyboards.inline.home_buttons import home_key
router = Router()


@router.callback_query(F.data == "check_join")
async def check_join_cb_answer(call: types.CallbackQuery):
    await bot.delete_message(
        chat_id=call.message.chat.id, message_id=call.message.message_id
    )
    await bot.send_message(
        chat_id=call.message.chat.id, text="Quyidagilardan birini tanlang! 👇",
        reply_markup=home_key
    )
