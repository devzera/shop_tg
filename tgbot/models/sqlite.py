import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('yo.db')
    cur = db.cursor()
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' user('
        ' id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' user_id INT,'
        ' username TEXT,'
        ' UNIQUE(user_id)'
        ')'
    )
    cur.execute(
        'CREATE TABLE IF NOT EXISTS'
        ' product('
        ' product_id INTEGER PRIMARY KEY AUTOINCREMENT,'
        ' title TEXT,'
        ' price TEXT,'
        ' puffs INT,'
        ' taste INT,'
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
        ' order('
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
        cur.execute(
            'INSERT INTO taste(taste)'
            ' VALUES (?)',
            tuple(data.values())
        )
        cur.execute(
            'INSERT INTO product_taste(taste)'
            ' VALUES (?)',
            tuple(data.values())
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
    return cur.execute('SELECT * FROM product').fetchall()


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
