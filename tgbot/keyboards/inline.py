from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def user_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    '🎫 Каталог товаров',
                    callback_data='get_catalog'
                )
            ],
            [
                InlineKeyboardButton(
                    '🧾 Заказы',
                    callback_data='get_orders'
                ),
                InlineKeyboardButton(
                    '🛒 Корзина',
                    callback_data='get_basket'
                )
            ]
        ]
    )
    return ikb


def admin_menu_ikb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    '🎫 Каталог товаров',
                    callback_data='get_catalog'
                )
            ],
            [
                InlineKeyboardButton(
                    '🧾 Заказы',
                    callback_data='get_orders'
                ),
                InlineKeyboardButton(
                    '🛒 Корзина',
                    callback_data='get_basket'
                )
            ],
            [
                InlineKeyboardButton(
                    '👑 Добавить товар(админка)',
                    callback_data='get_admin_panel'
                )
            ],
        ]
    )
    return ikb


def catalog_menu_ikb(data) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(row_width=5)
    print(data)
    if len(data) > 1:

        for taste in data[1:]:
            ikb.insert(
                InlineKeyboardButton(
                    taste['taste_title'],
                    callback_data=f'get_taste'
                                  f'_{data[0]["product_id"]}'
                                  f'_{taste["quantity_in_stock"]}'
                                  f'_{taste["taste_id"]}'
                )
            )

    ikb.add(
        InlineKeyboardButton(
            '🍬 Добавить вкус(админка)',
            callback_data=f'add_taste_{data[0]["product_id"]}'
        )
    )
    ikb.row(
        InlineKeyboardButton(
            '◀️',
            callback_data='get_catalog_previous'
        ),
        InlineKeyboardButton(
            'Поиск',
            callback_data='search_product'
        ),
        InlineKeyboardButton(
            '▶️',
            callback_data='get_catalog_next'
        )
    )
    ikb.add(
        InlineKeyboardButton(
            '🔙 Назад',
            callback_data='get_menu'
        )
    )

    return ikb


def taste_ikb(data) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    '🛒️ Добавить в корзину',
                    callback_data=f'add_to_basket_{data}'
                )
            ],
            [
                InlineKeyboardButton(
                    'Изменить(админка)',
                    callback_data='get_orders'
                )
            ],
            [
                InlineKeyboardButton(
                    '🔙 Назад',
                    callback_data='get_catalog'
                )
            ],
        ]
    )
    return ikb


def basket_ikb(for_btn) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(
        row_width=5
    )
    for item in for_btn:
        title, basket_id = item.split('_')

        ikb.add(
            InlineKeyboardButton(
                title,
                callback_data='get_catalog'
            )
        )
        ikb.add(
            InlineKeyboardButton(
                f'➕',
                callback_data=f'set_basket_inc_{basket_id}'
            )
        )
        ikb.insert(
            InlineKeyboardButton(
                f'➖',
                callback_data=f'set_basket_dec_{basket_id}'
            )
        )
        ikb.insert(
            InlineKeyboardButton(
                f'❌',
                callback_data=f'set_basket_del_{basket_id}'
            )
        )

    ikb.add(
        InlineKeyboardButton(
            '💴 Оплатить',
            callback_data='get_menu'
        )
    )
    ikb.add(
        InlineKeyboardButton(
            '🔙 Назад',
            callback_data='get_menu'
        )
    )

    return ikb
