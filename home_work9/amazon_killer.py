from flask import Flask, request
from datetime import datetime
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class NoSuchUser(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


@app.errorhandler(NoSuchUser)
def no_such_user_handler(e):
    return {"error": f"no such user with id={e.user_id}"}, 404


class NoSuchCart(Exception):
    def __init__(self, cart_id):
        self.cart_id = cart_id


@app.errorhandler(NoSuchCart)
def no_such_cart_handler(e):
    return {"error": f"no such cart with id={e.cart_id}"}, 404


class UserAPI(Resource):
    USERS_DATABASE = {}
    user_counter = 1

    def post(self):
        user = request.json
        user['user_id'] = self.user_counter
        response = {
            "registration_timestamp": datetime.now().isoformat(),
            "user_id": self.user_counter
        }
        user["registration_timestamp"] = response['registration_timestamp']
        self.USERS_DATABASE[self.user_counter] = user

        self.user_counter += 1

        return response, 201

    def get(self, user_id):
        try:
            user = self.USERS_DATABASE[user_id]
        except KeyError:
            raise NoSuchUser(user_id)
        else:
            return user

    def put(self, user_id):
        if user_id not in self.USERS_DATABASE:
            raise NoSuchUser(user_id)

        user = request.json
        self.USERS_DATABASE[user_id] = user

        return {"status": "success"}

    def delete(self, user_id):
        if user_id not in self.USERS_DATABASE:
            raise NoSuchUser(user_id)

        del self.USERS_DATABASE[user_id]

        return {"status": "success"}


class CartAPI(Resource):

    CARTS_DATABASE = {}
    cart_counter = 1

    def post(self):

        cart = request.json

        user_id = cart['user_id']
        if user_id not in UserAPI.USERS_DATABASE:
            raise NoSuchUser(user_id)

        cart['cart_id'] = self.cart_counter
        cart["creation_time"] = datetime.now().isoformat()

        self.CARTS_DATABASE[self.cart_counter] = cart

        self.cart_counter += 1

        response = {"cart_id": cart['cart_id'],
                    "creation_time": cart['creation_time']}
        return response, 201

    def get(self, cart_id):
        try:
            cart = self.CARTS_DATABASE[cart_id]
        except KeyError:
            raise NoSuchCart(cart_id)
        else:
            return cart

    def put(self, cart_id):
        if cart_id not in self.CARTS_DATABASE:
            raise NoSuchCart(cart_id)

        cart = request.json

        user_id = cart['user_id']
        if user_id not in UserAPI.USERS_DATABASE:
            raise NoSuchUser(user_id)

        self.CARTS_DATABASE[cart_id] = cart

        return {"status": "success"}

    def delete(self, cart_id):
        if cart_id not in self.CARTS_DATABASE:
            raise NoSuchCart(cart_id)

        del self.CARTS_DATABASE[cart_id]

        return {"status": "success"}


api.add_resource(UserAPI, '/users', '/users/<int:user_id>')
api.add_resource(CartAPI, '/carts', '/carts/<int:cart_id>')

if __name__ == '__main__':
    app.run(debug=True)
