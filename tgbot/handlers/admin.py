from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.inline import admin_menu_ikb
from tgbot.misc.states import ProductFSM
from tgbot.models.sqlite import db_create_product


async def admin_start(message: Message):
    await message.answer(
        f'YuotoBot - это бот, который'
        f' позволяет заказать продукцию'
        f' компании YUOTO',
        reply_markup=admin_menu_ikb()
    )


async def create_product(callback: CallbackQuery):
    await ProductFSM.title.set()
    await callback.message.answer(
        'Введите название:',
    )


async def set_product_title(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['title'] = message.text
    await ProductFSM.next()
    await message.answer(
        'Введите количество затяжек:',
    )


async def set_product_puffs(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['puffs'] = message.text
    await ProductFSM.next()
    await message.answer(
        'Введите цену:',
    )


async def set_product_price(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
    await ProductFSM.next()
    await message.answer(
        'Введите количество на складе:',
    )


async def set_product_amount(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await ProductFSM.next()
    await message.answer(
        'Введите описание:',
    )


async def set_product_desc(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
    await ProductFSM.next()
    await message.answer(
        'Введите артикул:',
    )


async def set_product_vendor(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['vendor_code'] = message.text
    await db_create_product(state)
    await state.finish()


async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        return
    await state.finish()
    await message.answer('ОК')


def register_admin(dp: Dispatcher):
    dp.register_callback_query_handler(
        create_product,
        lambda callback_query: callback_query.data == 'get_admin_panel',
        state=None
    )
    dp.register_message_handler(set_product_title, state=ProductFSM.title)
    dp.register_message_handler(set_product_puffs, state=ProductFSM.puffs)
    dp.register_message_handler(set_product_price, state=ProductFSM.price)
    dp.register_message_handler(set_product_amount, state=ProductFSM.amount)
    dp.register_message_handler(set_product_desc, state=ProductFSM.description)
    dp.register_message_handler(set_product_vendor, state=ProductFSM.vendor_code)
    dp.register_message_handler(cancel_handler, commands='отмена', state='*')
    dp.register_message_handler(
        cancel_handler,
        Text(equals='отмена', ignore_case=True),
        state='*'
    )
    dp.register_message_handler(
        admin_start,
        commands=["start"],
        state="*",
        is_admin=True
    )
