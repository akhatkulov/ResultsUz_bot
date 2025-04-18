from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_keyboard = [
    [
        InlineKeyboardButton(text="✅ Yes", callback_data="yes"),
        InlineKeyboardButton(text="❌ No", callback_data="no"),
    ]
]
are_you_sure_markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

adm_buttons_list = [
    [InlineKeyboardButton(text="📊Statistika", callback_data="stat")],
    [InlineKeyboardButton(text="📬Xabar yuborish", callback_data="send")],
    [InlineKeyboardButton(text="⚙️Kanallarni sozlash", callback_data="channels")],
    [
        InlineKeyboardButton(
            text="➕Adminlarni boshqarish", callback_data="sitting_admins"
        )
    ],
]

admin_buttons = InlineKeyboardMarkup(inline_keyboard=adm_buttons_list)

channel_control_buttons_list = [
    [InlineKeyboardButton(text="➕Kanal qo'shish", callback_data="channel_add")],
    [InlineKeyboardButton(text="➖Kanalni olib tashlash", callback_data="channel_del")],
]

channel_control = InlineKeyboardMarkup(inline_keyboard=channel_control_buttons_list)


def join_buttons(l):
    button_base = []

    for i, j in enumerate(l):
        button_base.append([InlineKeyboardButton(text=f"〽️ {i+1}-kanal", url=j)])

    button_base.append(
        [InlineKeyboardButton(text="✔️ Tekshirish", callback_data="check_join")]
    )
    res = InlineKeyboardMarkup(inline_keyboard=button_base)

    return res
