from flask import Flask, request
from datetime import datetime

amazon_killer = Flask(__name__)

USERS_DATABASE = {}
user_counter = 1


CARTS_DATABASE = {}
cart_counter = 1


class NoSuchUser(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class NoSuchCart(Exception):
    def __init__(self, cart_id):
        self.cart_id = cart_id


@amazon_killer.route('/users', methods=["POST"])
def create_user():
    global user_counter
    user = request.json
    user['user_id'] = user_counter
    response = {
        "registration_timestamp": datetime.now().isoformat(),
        "user_id": user_counter
    }
    user["registration_timestamp"] = response['registration_timestamp']
    USERS_DATABASE[user_counter] = user

    user_counter += 1

    return response, 201


@amazon_killer.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": f"no such user with id={e.user_id}"}, 404


@amazon_killer.route('/users/<int:user_id>')
def get_user(user_id):
    try:
        user = USERS_DATABASE[user_id]
    except KeyError:
        raise NoSuchUser(user_id)
    else:
        return user


@amazon_killer.route('/users/<int:user_id>', methods=["PUT"])
def update_user(user_id):
    if user_id not in USERS_DATABASE:
        raise NoSuchUser(user_id)

    user = request.json
    USERS_DATABASE[user_id] = user

    return {"status": "success"}


@amazon_killer.route('/users/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    if user_id not in USERS_DATABASE:
        raise NoSuchUser(user_id)

    del USERS_DATABASE[user_id]

    return {"status": "success"}


@amazon_killer.route('/carts', methods=["POST"])
def create_cart():
    global cart_counter

    cart = request.json

    user_id = cart['user_id']
    if user_id not in USERS_DATABASE:
        raise NoSuchUser(user_id)

    cart['cart_id'] = cart_counter
    cart["creation_time"] = datetime.now().isoformat()

    CARTS_DATABASE[cart_counter] = cart

    cart_counter += 1

    response = {"cart_id": cart['cart_id'],
                "creation_time": cart['creation_time']}
    return response, 201


@amazon_killer.errorhandler(NoSuchCart)
def no_such_cart_handler(e):
    return {"error": f"no such cart with id={e.cart_id}"}, 404


@amazon_killer.route('/carts/<int:cart_id>')
def get_cart(cart_id):
    try:
        cart = CARTS_DATABASE[cart_id]
    except KeyError:
        raise NoSuchCart(cart_id)
    else:
        return cart


@amazon_killer.route('/carts/<int:cart_id>', methods=["PUT"])
def update_cart(cart_id):
    if cart_id not in CARTS_DATABASE:
        raise NoSuchCart(cart_id)

    cart = request.json

    user_id = cart['user_id']
    if user_id not in USERS_DATABASE:
        raise NoSuchUser(user_id)

    CARTS_DATABASE[cart_id] = cart

    return {"status": "success"}


@amazon_killer.route('/carts/<int:cart_id>', methods=["DELETE"])
def delete_cart(cart_id):
    if cart_id not in CARTS_DATABASE:
        raise NoSuchCart(cart_id)

    del CARTS_DATABASE[cart_id]

    return {"status": "success"}


if __name__ == '__main__':
    amazon_killer.run(debug=True)
