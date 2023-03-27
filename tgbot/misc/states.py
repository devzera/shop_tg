from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductFSM(StatesGroup):
    title = State()
    puffs = State()
    price = State()
    amount = State()
    description = State()
    vendor_code = State()
