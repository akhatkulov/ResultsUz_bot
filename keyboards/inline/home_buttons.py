from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


home_keyboard_list = [
    [
        InlineKeyboardButton(text="➕ Test joylash", callback_data="add_test"),
    ],
    [
        InlineKeyboardButton(text="✅ Testga javob berish", callback_data="pass_test"),
    ],
    [
        InlineKeyboardButton(text="🔲 Testni yakunlash", callback_data="close_test"),
    ]
]
home_key = InlineKeyboardMarkup(inline_keyboard=home_keyboard_list)
