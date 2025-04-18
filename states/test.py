from aiogram.filters.state import StatesGroup, State


class AdminState(StatesGroup):
    are_you_sure = State()
    ask_ad_content = State()
    Add_Channel = State()
    Delete_Channel = State()
