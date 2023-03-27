from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message

from tgbot.keyboards.inline import basket_ikb, catalog_menu_ikb, user_menu_ikb
from tgbot.models.sqlite import (db_add_to_basket, db_dec_amount_product,
                                 db_del_amount_product, db_get_basket,
                                 db_inc_amount_product, sql_read)


async def user_start(message: Message):
    await message.answer(
        f'YuotoBot - это бот, который'
        f' позволяет заказать продукцию'
        f' компании YUOTO',
        reply_markup=user_menu_ikb()
    )


async def menu(callback: CallbackQuery):
    await callback.message.edit_text(
        f'YuotoBot - это бот, который'
        f' позволяет заказать продукцию'
        f' компании YUOTO',
        reply_markup=user_menu_ikb()
    )
    await callback.answer()


count = 0


def basket(products):

    text = ''
    for_btn = []
    total_price = 0
    total_amount = 0
    for product in products:
        for_btn.append(f'{product[1]}_{product[0]}')

        text += (
            f'Название: {product[1]}({product[4]})'
            f'\nЦена: {product[3]}'
            f'\nЗатяжек: {product[2]}'
            f'\nКоличество: {product[5]}'
            f'\n\n'
        )
        total_price += int(product[3]) * int(product[5])
        total_amount += int(product[5])

    if text:
        text += (
            f'Итоговая цена: {total_price}'
            f'\nИтоговое количество: {total_amount}'
        )
    else:
        text = 'Корзина пустая'

    return text, for_btn


async def get_product_catalog(callback: CallbackQuery):
    global count
    products = await sql_read()

    arrow = callback.data.split('_')[-1]

    if arrow == 'next':
        count += 1
    elif arrow == 'previous':
        count -= 1

    product = products[count % len(products)]

    text = (
        f'Название: {product[1]}'
        f'\nЦена: {product[2]}'
        f'\nКоличество затяжек: {product[3]}'
        f'\nОписание: {product[4]}'
        f'\nАртикул: {product[5]}'
    )

    taste_list = [{'product_id': product[0]}]
    for taste in products:
        data = {
            'quantity_in_stock': taste[-3],
            'taste_id': taste[-2],
            'taste_title': taste[-1]
        }
        taste_list.append(data)

    await callback.message.edit_text(
        text,
        reply_markup=catalog_menu_ikb(taste_list)
    )
    await callback.answer()


async def get_taste(callback: CallbackQuery):
    product_id = callback.data.split('_')[-3]
    quantity_in_stock = callback.data.split('_')[-2]
    taste_id = callback.data.split('_')[-1]


async def add_to_basket(callback: CallbackQuery):
    username = callback.from_user.username
    user_id = callback.from_user.id
    product_id = callback.data.split('_')[-1]
    data = (username, user_id, 11, product_id)
    await db_add_to_basket(data)


async def get_basket(callback: CallbackQuery):
    user_id = callback.from_user.id
    products = await db_get_basket(user_id)

    text, for_btn = basket(products)

    await callback.message.edit_text(
        text,
        reply_markup=basket_ikb(for_btn)
    )
    await callback.answer()


async def set_basket(callback: CallbackQuery):

    user_id = callback.from_user.id
    basket_id = callback.data.split('_')[-1]
    condition = callback.data.split('_')[-2]
    data = (basket_id, user_id)

    if condition == 'inc':
        await db_inc_amount_product(data)
    elif condition == 'dec':
        await db_dec_amount_product(data)
    else:
        await db_del_amount_product(data)

    products = await db_get_basket(user_id)

    text, for_btn = basket(products)

    await callback.message.edit_text(
        text,
        reply_markup=basket_ikb(for_btn)
    )
    await callback.answer()


def register_user(dp: Dispatcher):
    dp.register_callback_query_handler(
        get_product_catalog,
        lambda callback_query: callback_query.data.startswith('get_catalog')
    )
    dp.register_callback_query_handler(
        get_taste,
        lambda callback_query: callback_query.data.startswith('set_basket')
    )
    dp.register_callback_query_handler(
        add_to_basket,
        lambda callback_query: callback_query.data.startswith('add_to_basket')
    )
    dp.register_callback_query_handler(
        get_basket,
        lambda callback_query: callback_query.data == 'get_basket'
    )
    dp.register_callback_query_handler(
        set_basket,
        lambda callback_query: callback_query.data.startswith('set_basket')
    )
    dp.register_callback_query_handler(
        menu,
        lambda callback_query: callback_query.data == 'get_menu'
    )
    dp.register_message_handler(user_start, commands=["start"], state="*")
