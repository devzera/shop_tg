import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('yo.db')
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' user('
        ' user_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' username TEXT'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' product('
        ' product_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' title TEXT,'
        ' price INT,'
        ' puffs INT,'
        ' description TEXT,'
        ' vendor_code TEXT'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' taste('
        ' taste_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' taste TEXT'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' product_taste('
        'quantity_in_stock INT,'
        ' product_id INT,'
        ' taste_id INT,'
        ' FOREIGN KEY (product_id) REFERENCES product (product_id),'
        ' FOREIGN KEY (taste_id) REFERENCES taste (taste_id)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' basket('
        ' basket_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' quantity_in_cart INT,'
        ' product_id INT,'
        ' user_id INT,'
        ' FOREIGN KEY (product_id) REFERENCES product (product_id),'
        ' FOREIGN KEY (user_id) REFERENCES user (user_id),'
        ' UNIQUE(product_id, user_id)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' user_order('
        ' order_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' quantity_in_order INT,'
        ' product_id INT,'
        ' user_id INT,'
        ' FOREIGN KEY (product_id) REFERENCES product (product_id),'
        ' FOREIGN KEY (user_id) REFERENCES user (user_id)'
        ')'
    )
    db.commit()


async def db_create_product(state):
    async with state.proxy() as data:
        cur.execute(
            'INSERT INTO product('
            'title, price,'
            ' puffs, description,'
            ' vendor_code)'
            ' VALUES (?, ?, ?, ?, ?)',
            tuple(data.values())
        )
    db.commit()


async def db_create_taste(state):
    async with state.proxy() as data:
        data = tuple(data.values())
        taste_title = data[0]
        num_of_flavors_in_stock = data[1]
        product_id = data[2]

        taste_created = cur.execute(
            'SELECT taste_id, taste_title FROM taste'
            ' WHERE taste = ?',
            (taste_title,)
        ).fetchall()

        if not taste_created:

            cur.execute(
                'INSERT INTO taste(taste)'
                ' VALUES (?)',
                (taste_title, )
            )

        taste_id = taste_created[0] or cur.lastrowid

        cur.execute(
            'INSERT INTO product_taste('
            'quantity_in_stock, product_id, taste_id)'
            ' VALUES (?, ?, ?)',
            (num_of_flavors_in_stock, product_id, taste_id)
        )

    db.commit()


async def db_add_to_basket(data):
    cur.execute(
        'INSERT INTO basket('
        'product_amount, product_id, user_id)'
        ' VALUES (?, ?, ?)',
        data
    )
    db.commit()


async def sql_read():

    return cur.execute(
        'SELECT product.product_id, product.title,'
        ' product.price, product.puffs,'
        ' product.description, product.vendor_code,'
        ' product_taste.quantity_in_stock,'
        ' taste.taste_id, taste.taste'
        ' FROM product'
        ' LEFT JOIN product_taste ON'
        ' product.product_id = product_taste.product_id'
        ' LEFT JOIN taste ON'
        ' product_taste.taste_id = taste.taste_id'
    ).fetchall()


async def sql(data):
    taste_queryset = cur.execute(
        'SELECT product.product_id, product.title,'
        ' product.price, product.puffs,'
        ' product.description, product.vendor_code,'
        ' product_taste.quantity_in_stock,'
        ' taste.taste_id, taste.taste'
        ' FROM product_taste'
        ' INNER JOIN product ON'
        ' product_taste.product_id = product.product_id'
        ' INNER JOIN taste ON'
        ' product_taste.taste_id = taste.taste_id'
        ' WHERE product_taste.product_id = ? '
        ' AND product_taste.taste_id = ?',
        data
    ).fetchall()

    return taste_queryset


async def db_get_basket(user_id):
    basket_queryset = cur.execute(
        f'SELECT basket.basket_id, SUM(basket.product_amount)'
        f' product.title, product.puffs,'
        f' product.price, product.vendor_code,'
        f' FROM basket'
        f' INNER JOIN product ON'
        f' basket.product_id = product.product_id'
        f' WHERE user_id = ?'
        f' GROUP BY basket.product_id'
        f' ORDER BY product.title',
        (user_id, )
    ).fetchall()

    return basket_queryset


async def db_inc_amount_product(data):
    cur.execute(
        'UPDATE basket'
        ' SET product_amount = product_amount + 1'
        ' WHERE id = ? AND user_id = ?',
        data
    )
    db.commit()


async def db_dec_amount_product(data):
    cur.execute(
        'UPDATE basket'
        ' SET product_amount = product_amount - 1'
        ' WHERE id = ? AND user_id = ?',
        data
    )
    cur.execute(
        'DELETE FROM basket'
        ' WHERE id = ? AND user_id = ? AND product_amount = 0',
        data
    )
    db.commit()


async def db_del_amount_product(data):
    cur.execute(
        'DELETE FROM basket'
        ' WHERE id = ? AND user_id = ?',
        data
    )
    db.commit()
