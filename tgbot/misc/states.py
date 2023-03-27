from aiogram.dispatcher.filters.state import State, StatesGroup


class ProductFSM(StatesGroup):
    title = State()
    price = State()
    puffs = State()
    description = State()
    vendor_code = State()


class TasteFSM(StatesGroup):
    taste = State()
    num_of_flavors_in_stock = State()
