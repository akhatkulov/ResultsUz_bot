import logging
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loader import bot
from keyboards.inline.buttons import admin_buttons, channel_control
from states.test import AdminState
from filters.admin import IsBotAdminFilter
from utils.db.alchemy import (
    user_count,
    get_all_user,
    get_channel,
    put_channel,
    get_channel_with_id,
    delete_channel,
    get_admins,
    manage_admin,
)
from data.config import ADMIN

router = Router()


@router.message(Command("admin"), IsBotAdminFilter())
async def admin_panel(msg: types.Message):
    await bot.send_message(
        chat_id=msg.chat.id,
        text="Salom, Admin hush kelibsiz",
        reply_markup=admin_buttons,
    )


@router.message(Command("list_admins"), IsBotAdminFilter())
async def get_admins_list(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        l_o_a = get_admins()
        print(l_o_a)
        await bot.send_message(
            chat_id=msg.chat.id, text=f"Adminlar ro'yxati\n\n{l_o_a}"
        )


@router.message(Command("add_admin"), IsBotAdminFilter())
async def get_admins_list(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        try:
            target_cid = msg.text.split()[1]
            print(target_cid)
            manage_admin(cid=int(target_cid), action="add")
            await bot.send_message(chat_id=msg.chat.id, text=f"Bajarildi")
        except Exception as e:
            await bot.send_message(chat_id=ADMIN, text=f"{e}")
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Sizda bunday imkoniyat yo'q")


@router.message(Command("del_admin"), IsBotAdminFilter())
async def get_admins_list(msg: types.Message):
    if int(msg.chat.id) == ADMIN:
        try:
            target_cid = msg.text.split()[1]
            manage_admin(cid=int(target_cid), action="rm")
            await bot.send_message(chat_id=msg.chat.id, text=f"")
        except Exception as e:
            await bot.send_message(chat_id=ADMIN, text=e)
    else:
        await bot.send_message(chat_id=msg.chat.id, text="Sizda bunday imkoniyat yo'q")


@router.callback_query(F.data == "stat")
async def show_stat(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id, text=f"👥Foydalanuvchilar soni: {user_count()}"
    )


@router.callback_query(F.data == "send")
async def show_stat(call: types.CallbackQuery, state: FSMContext):

    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Yubormoqchi bo'lgan xabaringizni yuboring, jarayonni bekor qilish uchun /admin !",
    )
    await state.set_state(AdminState.ask_ad_content)


@router.callback_query(F.data == "channels")
async def show_stat(call: types.CallbackQuery):
    r = get_channel_with_id()
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=f"Kanallar ro'yxati:{r}",
        reply_markup=channel_control,
    )


@router.callback_query(F.data == "channel_add")
async def func_channel_add(call: types.CallbackQuery, state: FSMContext):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text="Kanal CIDsini yuboring, jarayonni bekor qilish uchun /admin !",
    )
    await state.set_state(AdminState.Add_Channel)


@router.callback_query(F.data == "channel_del")
async def func_channel_del(call: types.CallbackQuery, state: FSMContext):
    res_text = f"{get_channel_with_id()}\n\nO'chirmoqchi bo'lgan kanalingiz ID raqamini bering, jarayonni bekor qilish uchun /admin!"
    await bot.send_message(chat_id=call.message.chat.id, text=res_text)
    await state.set_state(AdminState.Delete_Channel)


@router.callback_query(F.data == "sitting_admins", IsBotAdminFilter())
async def sitting_admins(call: types.CallbackQuery):
    await bot.send_message(
        chat_id=call.message.chat.id,
        text=f"Bu hususiyatdan faqat {ADMIN} foydalana oladi!\n\n /list_admins -- Adminlar ro'yxatini ko'rish\n/add_admin [CID] -- Admin qo'shish\n/del_admin [CID] -- Adminni olib tashlash",
    )


@router.message(AdminState.ask_ad_content, IsBotAdminFilter())
async def send_ad_to_users(message: types.Message, state: FSMContext):
    if message.text != "/admin" and message.text != "/start":
        users = get_all_user()
        count = 0
        for user in users:
            try:
                await message.send_copy(chat_id=user)
                count += 1
                await asyncio.sleep(0.033)
            except Exception as error:
                logging.info(f"Ad did not send to user: {user}. Error: {error}")
        await message.answer(
            text=f"Reklama {count} ta foydalauvchiga muvaffaqiyatli yuborildi."
        )
    await state.clear()


@router.message(AdminState.Add_Channel, IsBotAdminFilter())
async def func_add_channel_process(message: types.Message, state: FSMContext):
    if message.text != "/admin" and message.text != "/start":
        try:
            put_channel(channel=message.text)
            await bot.send_message(
                chat_id=message.chat.id,
                text=f"{message.text} majburiy kanallar ro'yxatiga qo'shildi ✅",
            )
        except Exception as error:
            logging.info(f"Set Channel -- {error}")
    await state.clear()


@router.message(AdminState.Delete_Channel, IsBotAdminFilter())
async def func_delete_channel_process(message: types.Message, state: FSMContext):
    if message.text != "/admin" and message.text != "/start":
        try:
            x = int(message.text)
            if delete_channel(ch_id=x):
                await bot.send_message(
                    chat_id=message.chat.id, text="Kanal olib tashlandi"
                )
            else:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text="Xatolik! IDni to'g'ri kiritdingizmi tekshiring!",
                )
        except Exception as error:
            logging.info(f"Delete Channel: {error}")

    await state.clear()
