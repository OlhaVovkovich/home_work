# from datetime import datetime

import psycopg2
import psycopg2.extras
from psycopg2 import sql


conn = psycopg2.connect(dbname='postgres', user='postgres',
                        password='password', host='0.0.0.0')
cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)


def create_user(user_info: dict):
    query_users = (
        'INSERT INTO users (name, email, registration_time)'
        'VALUES (%(name)s, %(email)s, %(registration_time)s)'
        'RETURNING id;'
    )
    cursor.execute(query_users, user_info)

    user_id = dict(cursor.fetchone())['id']

    conn.commit()

    return user_id


def read_user_info(id_: int):
    query_select = 'SELECT * FROM users WHERE id = %s'

    cursor.execute(query_select, (id_,))
    record = cursor.fetchone()

    return record


def update_user(new_info: dict, _id: int):

    sql_update_query = sql.SQL('UPDATE users SET {data} WHERE id = {id}')

    data = sql.SQL(', ').join(
        (sql.Identifier(k) + sql.Placeholder(k)).join('=') for k in new_info.keys()
    )

    sql_query = sql_update_query.format(data=data, id=sql.Placeholder('id'))

    new_info.update(id=_id)

    cursor.execute(sql_query, new_info)

    updated_rowcount = cursor.rowcount

    conn.commit()

    return updated_rowcount


def delete_user(_id):
    delete_query = 'DELETE FROM users WHERE id = %s'
    cursor.execute(delete_query, (_id,))

    deleted_rowcount = cursor.rowcount

    conn.commit()

    return deleted_rowcount


def create_cart(cart: dict):
    query_creat_cart = """
    INSERT INTO cart (creation_time, user_id) VALUES (%(creation_time)s, %(user_id)s)
    RETURNING id;
    """

    cursor.execute(query_creat_cart, dict(user_id=cart['user_id'], creation_time=cart['creation_time']))

    cart_id = cursor.fetchone()[0]

    query_creat_cart_detail = """
    INSERT INTO cart_details (cart_id, price, product) VALUES (%(cart_id)s, %(price)s, %(product)s)
    """

    for cart_detail in cart['cart_details']:
        cart_detail.update(cart_id=cart_id)
        cursor.execute(query_creat_cart_detail, cart_detail)

    conn.commit()

    return cart_id


# не бачу сенсу оновлювати записи із таблиці cart, вона містить тільки службову інформацію
def update_cart(cart: dict):
    sql_update_query = sql.SQL('UPDATE cart_details SET {data} WHERE id = {id}')

    updated_rowcount = 0

    for cart_detail in cart['cart_details']:
        data = sql.SQL(', ').join(
            (sql.Identifier(k) + sql.Placeholder(k)).join('=') for k in cart_detail.keys()
        )

        sql_query = sql_update_query.format(data=data, id=sql.Placeholder('id'))

        cursor.execute(sql_query, cart_detail)

        updated_rowcount += cursor.rowcount

    conn.commit()

    return updated_rowcount


def read_cart(_id: int):
    query_select_cart = 'SELECT * FROM cart WHERE id = %s'

    cursor.execute(query_select_cart, (_id,))
    cart = dict(cursor.fetchone())

    query_select_cart_details = 'SELECT * FROM cart_details WHERE cart_id = %s'
    cursor.execute(query_select_cart_details, (_id,))

    cart_details = cursor.fetchall()
    cart_details = [dict(cart_detail) for cart_detail in cart_details]

    cart['cart_details'] = cart_details

    return cart


def delete_cart(_id: int):
    deleted_rows = 0

    delete_query_cart_details = 'DELETE FROM cart_details WHERE cart_id = %s'
    cursor.execute(delete_query_cart_details, (_id,))
    deleted_rows += cursor.rowcount

    delete_query_cart = 'DELETE FROM cart WHERE id = %s'
    cursor.execute(delete_query_cart, (_id,))
    deleted_rows += cursor.rowcount

    conn.commit()

    return deleted_rows


# record_to_insert = (6, 'O', 'vovkov@gmail.com', '2020-01-01 11:45:00')
# create_user({'name': 'Olya', 'email': 'vovkov@gmail.com', 'registration_time': datetime.now()})

# cursor.execute("SELECT * FROM users")
# print(cursor.fetchall())
# print(dict(read_user_info(1)))
# update_user({'email': 'vovkovych@gmail.com'}, _id=4)
# print(read_user_info(4))
# delete_user(4)
# print(read_user_info(4))


# create_cart(
#     {
#         'creation_time': datetime.now(),
#         'user_id': 1,
#         'cart_details': [
#             {'price': 100, 'product': 'macbook'}
#         ]
#     }
# )

# print(update_cart(
#     {
#         'cart_details': [
#             {'id': 10, 'price': 3100, 'product': 'macbook'},
#             {'id': 11, 'price': 4100, 'product': 'macbook'},
#             {'id': 12, 'price': 5100, 'product': 'macbook'},
#         ]
#     }
# ))

# print(read_cart(10))

# print(delete_cart(2))
