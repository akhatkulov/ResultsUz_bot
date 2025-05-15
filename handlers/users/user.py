from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loader import bot
from keyboards.inline.home_buttons import home_key
from states.test import UserState
from utils.helper.func import test_checker
from utils.db.alchemy import get_test,create_test,change_test_info
import json
from loader import bot
from data.config import ADMIN
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

@router.callback_query(F.data == "add_test")
async def add_test(call: types.CallbackQuery,state:FSMContext):
    await call.message.answer("Test javoblarini kiriting.\n<b>Namuna: aaabbabbabba</b>")
    await state.set_state(UserState.add_test)



@router.message(UserState.add_test)
async def add_test_state(msg: types.Message,state:FSMContext):
    test_code = create_test(owner=int(msg.chat.id),answer=msg.text)
    await msg.answer(f"Foydalanuvchi javobni quyidagi tartib raqam orqali tekshirib olishi mumkin.\n\n<b>{test_code}</b>",reply_markup=home_key)
    await state.clear()

@router.callback_query(F.data == "pass_test")
async def add_test(call: types.CallbackQuery,state:FSMContext):
    await call.message.answer("F.I.SHni yuboring\n<b>Namuna: Axatkulov Mexroj Sehroj o'g'li</b>")
    await state.set_state(UserState.get_name)

@router.message(UserState.get_name)
async def get_name(msg: types.CallbackQuery, state: FSMContext):
    await state.update_data(name=msg.text)
    await msg.answer("Testga quyidagicha javob yuboring:\n\n<b>tartib raqam#harflar</b>")
    await state.set_state(UserState.pass_test)

@router.message(UserState.pass_test)
async def pass_test_state(msg: types.Message, state: FSMContext):
    data_state = await state.get_data()
    name = data_state.get("name")
    async def invalid_format():
        return await msg.answer(
            "🚫Javobni noto'g'ri formatda berdingiz. Javoblarni quyidagi formatda jo'nating:\n"
            "...................................................................\n"
            "👉 Test tartib raqami - faqat raqamlardan iborat\n"
            "👉 # - maxsus belgi\n"
            "👉 javoblar - faqat harflardan iborat",
            reply_markup=home_key
        )

    text = msg.text
    if text.count("#") != 1:
        return await invalid_format()

    code, answer = text.split("#")

    if not code.isdigit():
        return await invalid_format()

    test = get_test(id=int(code))
    if not test or test.status != "Open":
        return await msg.answer("Ushbu test muddati tugagan!", reply_markup=home_key)

    if len(answer) != len(test.answer):
        return await invalid_format()

    res = test_checker(answer=answer, target=test.answer)
    report = (
        f"Siz bergan javoblar qabul qilindi. Natijangiz quyidagicha:\n\n"
        f"✅ To'g'ri javoblar: {len(res['true'])} ta\n"
        f"❌ Noto'g'ri javoblar: {len(res['false'])} ta\n"
        f".......................................... \n"
        f"✅ To'g'ri topilganlar:\n➖ {','.join(map(str, res['true']))}\n"
        f".......................................... \n"
        f"❌ Noto'g'ri topilganlar:\n➖ {','.join(map(str, res['false']))}"
    )


    report_for_admin = (
        f"{name} bergan javoblar qabul qilindi. Natijangiz quyidagicha:\n\n"
        f"✅ To'g'ri javoblar: {len(res['true'])} ta\n"
        f"❌ Noto'g'ri javoblar: {len(res['false'])} ta\n"
        f".......................................... \n"
        f"✅ To'g'ri topilganlar:\n➖ {','.join(map(str, res['true']))}\n"
        f".......................................... \n"
        f"❌ Noto'g'ri topilganlar:\n➖ {','.join(map(str, res['false']))}"
    )

    await bot.send_message(chat_id=test.owner,text=report_for_admin)
    await msg.answer(report, reply_markup=home_key)
    change_test_info(id=int(code),type_data="participant",value={name:len(res['true'])})
    await state.clear()



@router.callback_query(F.data == 'close_test')
async def close_test(call: types.CallbackQuery, state:FSMContext):
    await call.message.answer("Testning tartib raqamini kiriting.\n<b>Namuna: 2000001</b>")
    await state.set_state(UserState.close_test)

@router.message(UserState.close_test)
async def close_test_state(msg: types.Message,state:FSMContext):
    if msg.text.isdigit():
        test = get_test(id=int(msg.text))
        if test and test.owner == int(msg.chat.id):
            if test.status == "Open":
                report = f"{msg.text} tartib raqamdagi testning natijalari.\n\n"
                
                base = json.loads(test.participants)
                users = sorted(base,reverse=True)
                i = 1
                for user in users:
                    report+= f"{i}. {user} - ✅{base[user]} ❌{len(test.answer)-int(base[user])}\n"
                    i+=1
                print(report)
                await msg.answer(report)

                answer_report = f"{msg.text} tartib raqamdagi test yakunlandi.\nTo'g'ri javoblar:\n\n"

                for i in range(0,len(test.answer)):
                    answer_report += f"{i+1}.{test.answer[i]}\n"
                
                await msg.answer(answer_report,reply_markup=home_key)

                change_test_info(id=int(msg.text),type_data="status",value="Close")
            else:
                report = f"{msg.text} tartib raqamdagi testning natijalari.\n\n"
                
                base = json.loads(test.participants)
                users = sorted(base,reverse=True)
                i = 1
                for user in users:
                    report+= f"{i}. {user} - ✅{base[user]} ❌{len(test.answer)-int(base[user])}\n"
                    i+=1
                print(report)
                await msg.answer(report)

                answer_report = f"{msg.text} tartib raqamdagi test yakunlandi.\nTo'g'ri javoblar:\n\n"

                for i in range(0,len(test.answer)):
                    answer_report += f"{i+1}.{test.answer[i]}\n"
                
                await msg.answer(answer_report,reply_markup=home_key)
                await msg.answer("Bu test allaqachon yakunlanib bo'lingan!!!")
        else:
            await msg.answer("Bu testni siz yakunlay olmaysiz!",reply_markup=home_key)
    else:
        await msg.answer("Bunday tartib raqam mavjud emas",reply_markup=home_key)
    
    await state.clear()